from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Sum
from ..models import AssetClass, Currency, Operation, Pocket, Asset, AssetAllocation
from authentication.models import UserProfile

from decimal import Decimal
import yfinance as yf

from ..lib.AssetCalculator import AssetCalculator

def process_operation(data: dict, owner):
    if data['operation_type'] == 'buy':
        add_objects(data, owner)
    elif data['operation_type'] == 'sell':
        ...


def add_objects(data: dict, owner):

    try:
        asset_info = yf.Ticker(data['ticker']).info
        asset_name = asset_info['longName']
        currency = asset_info['currency']

    except Exception as e:
        raise e

    try:
        # ASSET
        # Check if asset exists in the database
        asset_query = Asset.objects.filter(
            ticker=data['ticker'],
            name=asset_name,
            asset_class=data['asset_class'],
            currency=Currency.objects.get(name=data['currency']))

        if not asset_query.exists():
            Asset.objects.create(
                ticker=data['ticker'],
                name=asset_name,
                asset_class=data['asset_class'],
                currency=Currency.objects.get(name=data['currency']))
            
        pocket = Pocket.objects.get(name=data['pocket_name'], owner=owner)

        # POCKET FEE
        if data['fee'] != 0:
            if data['currency'] == pocket.currency.name:
                pocket.fees += Decimal(data['fee'])
            else:
                pocket.fees += Decimal(data['fee'] * data['purchase_currency_price'])
            
            pocket.save()
  
        
            # TODO: Przetestować 

        # ASSET ALLOCATION
        # Check if asset allocation exists in the database
        asset_allocation_query = AssetAllocation.objects.filter(
            pocket=pocket,
            asset=Asset.objects.get(ticker=data['ticker']))

        if asset_allocation_query.exists():
            asset_allocation = asset_allocation_query.first()

            # Update the average purchase price
            average_purchase_price = _weighted_average(
                values=[asset_allocation.average_purchase_price,
                        Decimal(data['price'])],
                weights=[asset_allocation.quantity, Decimal(data['quantity'])])

            asset_allocation.average_purchase_price = Decimal(
                average_purchase_price)

            asset_allocation.quantity += Decimal(data['quantity'])
            asset_allocation.fee += Decimal(data['fee'])

            # Update the average purchase currency price
            average_purchase_currency_price = _weighted_average(
                values=[asset_allocation.average_purchase_currency_price,
                        Decimal(data['purchase_currency_price'])],
                weights=[asset_allocation.quantity, Decimal(data['quantity'])])

            asset_allocation.average_purchase_currency_price = Decimal(
                average_purchase_currency_price)

            asset_allocation.save()
        else:
            # Create new asset allocation
            AssetAllocation.objects.create(
                pocket=pocket,
                asset=Asset.objects.get(ticker=data['ticker']),
                quantity=data['quantity'],
                average_purchase_price=data['price'],
                average_purchase_currency_price=data['purchase_currency_price'],
                fee=data['fee']
            )

        return True

    except Exception as e:
        raise e


def _weighted_average(values: list, weights: list):
    return sum(value * weight for value, weight in zip(values, weights)) / sum(weights)


def currencies_prices_update(referece_currency: str = 'PLN'):
    currencies = Currency.objects.all()
    for currency in currencies:
        currency.reference_currency_name = referece_currency
        if currency.name != referece_currency:
            yf_exchange_info = yf.Ticker(
                f"{currency.name}{referece_currency}=X").info
            currency.exchange_rate = Decimal(yf_exchange_info["bid"])
            currency.save()
        else:
            currency.exchange_rate = 1.0
            currency.save()


def update_assets(pocket_name: str, owner: UserProfile):
    pocket = Pocket.objects.get(name=pocket_name, owner=owner)

    # Update the exchange rate of the currencies
    currencies_prices_update(pocket.currency.name)

    # Update the current price of the assets
    asset_allocation_query = AssetAllocation.objects.filter(
        pocket=pocket)

    if asset_allocation_query.exists():
        total_portfolio_value = 0

        for asset_allocation in asset_allocation_query:
            calculator = AssetCalculator(asset_allocation)

            # Update the current price of the asset
            asset_allocation.asset.current_price = calculator.update_price()
            asset_allocation.asset.save()

            asset_allocation.total_value_XXX = calculator.get_total_value_in_base_currency()
            asset_allocation.daily_change_percent = calculator.get_daily_change_percent()
            asset_allocation.daily_change_XXX = calculator.get_daily_change_in_base_currency()
            asset_allocation.rate_of_return = calculator.get_rate_of_return()
            asset_allocation.rate_of_return_XXX = calculator.get_rate_of_return_in_base_currency()
            asset_allocation.profit_XXX = calculator.get_profit_in_base_currency()
            asset_allocation.save()

            total_portfolio_value += asset_allocation.total_value_XXX

        for asset_allocation in asset_allocation_query:
            asset_allocation.participation = asset_allocation.total_value_XXX / \
                total_portfolio_value * 100
            asset_allocation.save()
    else:

        ...

    ...
