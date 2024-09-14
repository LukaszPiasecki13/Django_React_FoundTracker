from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Sum
from ..models import AssetClass, Currency, Operation, Pocket, Asset, AssetAllocation
from authentication.models import UserProfile

from decimal import Decimal
import yfinance as yf

from .AssetCalculator import AssetCalculator


class AssetProcessor:
    def __init__(self, owner: UserProfile,  data: dict = {} ):
        self.owner = owner
        if data:
            self.data = data
        else:
            ...

    def buy_operation(self):
        asset_name = self._get_asset_name(ticker=self.data['ticker'])

        try:
            # ASSET
            # Check if asset exists in the database
            asset_query = Asset.objects.filter(
                ticker=self.data['ticker'],
                name=asset_name,
                asset_class=self.data['asset_class'],
                currency=Currency.objects.get(name=self.data['currency']))

            if not asset_query.exists():
                Asset.objects.create(
                    ticker=self.data['ticker'],
                    name=asset_name,
                    asset_class=self.data['asset_class'],
                    currency=Currency.objects.get(name=self.data['currency']))
        except Exception as e:
            raise e

        try:
            # POCKET FEE
            pocket = Pocket.objects.get(
                name=self.data['pocket_name'], owner=self.owner)
            if self.data['fee'] != 0:
                if self.data['currency'] == pocket.currency.name:
                    pocket.fees += Decimal(self.data['fee'])
                else:
                    pocket.fees += Decimal(self.data['fee']
                                           * self.data['purchase_currency_price'])

                pocket.save()

        except Exception as e:
            raise e

        try:
            # ASSET ALLOCATION
            # Check if asset allocation exists in the database
            asset_allocation_query = AssetAllocation.objects.filter(
                pocket=pocket,
                asset=Asset.objects.get(ticker=self.data['ticker']))

            if not asset_allocation_query.exists():
                # Create new asset allocation
                AssetAllocation.objects.create(
                    pocket=pocket,
                    asset=Asset.objects.get(ticker=self.data['ticker']),
                    quantity=self.data['quantity'],
                    average_purchase_price=self.data['price'] +
                    self.data['fee']/self.data['quantity'],
                    average_purchase_currency_price=self.data['purchase_currency_price'],
                    fee=self.data['fee']
                )

            elif asset_allocation_query.exists():
                asset_allocation = asset_allocation_query.first()

                # Read the asset operations from the database
                buy_transactions, sell_transactions = self._get_asset_operations(
                    self.data['pocket_name'], self.owner, self.data['ticker'])
                
                # Add current transaction to the list of buy transactions
                buy_transactions.append((self.data['price'], self.data['quantity'], self.data['fee']))

                # Calculate the average purchase price
                average_purchase_price = self._calculate_average_purchase_price(
                    buy_transactions, sell_transactions)

                asset_allocation.average_purchase_price = Decimal(
                    average_purchase_price)

                # Update the average purchase currency price
                average_purchase_currency_price = _weighted_average(
                    values=[asset_allocation.average_purchase_currency_price,
                            Decimal(self.data['purchase_currency_price'])],
                    weights=[asset_allocation.quantity, Decimal(self.data['quantity'])])

                asset_allocation.average_purchase_currency_price = Decimal(
                    average_purchase_currency_price)
                
                # Update the quantity and fee
                asset_allocation.quantity += Decimal(self.data['quantity'])
                asset_allocation.fee += Decimal(self.data['fee'])

                asset_allocation.save()

        except Exception as e:
            raise e

        return True

    def subtract_objects(self):
        asset_name = self._get_asset_name(ticker=self.data['ticker'])

        try:
            # ASSET
            # Check if asset exists in the database
            asset_query = Asset.objects.filter(
                ticker=self.data['ticker'],
                name=asset_name,
                asset_class=self.data['asset_class'],
                currency=Currency.objects.get(name=self.data['currency']))

            if not asset_query.exists():
                raise ValueError("Asset does not exist in the database")
            
        except Exception as e:
            raise e
        
        try:
            pocket = Pocket.objects.get(name=self.data['pocket_name'], owner=self.owner)

            # POCKET FEE
            if self.data['fee'] != 0:
                if self.data['currency'] == pocket.currency.name:
                    pocket.fees += Decimal(self.data['fee'])
                else:
                    pocket.fees += Decimal(self.data['fee']
                                        * self.data['purchase_currency_price'])

        except Exception as e:
            raise e

        try:
            # ASSET ALLOCATION
            # Check if asset allocation exists in the database
            asset_allocation_query = AssetAllocation.objects.filter(
                pocket=pocket,
                asset=Asset.objects.get(ticker=self.data['ticker']))

            if asset_allocation_query.exists():
                asset_allocation = asset_allocation_query.first()

                # Read the asset operations from the database
                buy_transactions, sell_transactions = self._get_asset_operations(
                    self.data['pocket_name'], self.owner, self.data['ticker'])
                
                # Add current transaction to the list of buy transactions
                sell_transactions.append((self.data['price'], self.data['quantity'], self.data['fee']))

                # Calculate the average purchase price
                average_purchase_price = self._calculate_average_purchase_price(
                    buy_transactions, sell_transactions)

                asset_allocation.average_purchase_price = Decimal(
                    average_purchase_price)
                
                asset_allocation.fee += Decimal(self.data['fee'])

                check_operation_indicator = asset_allocation.quantity - \
                    Decimal(self.data['quantity'])
                
                if check_operation_indicator == 0:
                    asset_allocation.delete()

                    # Delete asset if quantity is 0
                    Asset.objects.get(ticker=self.data['ticker']).delete()

                elif check_operation_indicator > 0:
                    asset_allocation.quantity -= Decimal(self.data['quantity'])
                    asset_allocation.save()
                    ...
                    # TODO: Dodawanie pieniędzy do portfela ze sprzedaży
                elif check_operation_indicator < 0:
                    raise ValueError("Not enough assets to sell")

            else:
                raise ValueError("Asset allocation does not exist in the database")

        except Exception as e:
            raise e
        
        pocket.save()
        return True

    def add_funds(self):
        pocket = Pocket.objects.get(name=self.data['pocket_name'], owner=self.owner)
        pocket.free_cash += Decimal(self.data['quantity'])
        pocket.fees += Decimal(self.data['fee'])
        pocket.save()
        return True
    
    def withdraw_funds(self):
        pocket = Pocket.objects.get(name=self.data['pocket_name'], owner=self.owner)
        if pocket.free_cash < Decimal(self.data['quantity']):
            raise ValueError("Not enough free cash to withdraw")
        else:
            pocket.free_cash -= Decimal(self.data['quantity'])
            pocket.fees += Decimal(self.data['fee'])
            pocket.save()
            return True

    def update_assets(self, pocket_name: str):
        pocket = Pocket.objects.get(name=pocket_name, owner=self.owner)

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

    @staticmethod
    def _get_asset_name(ticker: str):
        try:
            asset_info = yf.Ticker(ticker).info
            asset_name = asset_info['longName']
            currency = asset_info['currency']
        except Exception as e:
            raise e

        return asset_name
    
    @staticmethod
    def _get_asset_operations(pocket_name: str, owner: UserProfile, ticker: str):
        operations = Operation.objects.filter(
            owner=owner,
            pocket_name=pocket_name,
            ticker=ticker)
        ...
        sell_transactions = []
        buy_transactions = []

        for operation in operations:
            if operation.operation_type == 'buy':
                buy_transactions.append(
                    (operation.price, operation.quantity, operation.fee))
            elif operation.operation_type == 'sell':
                sell_transactions.append(
                    (operation.price, operation.quantity, operation.fee))

        return buy_transactions, sell_transactions

    @staticmethod
    def _calculate_average_purchase_price(buy_transactions: list, sell_transactions: list = []) -> float:
        """
        Calculate the average stock price after considering purchase and sale transactions, including transaction fees.

        :param buy_transactions: List of tuples (price_per_share, number_of_shares, fee) for each purchase transaction.
        :param sell_transactions: Optional list of tuples (price_per_share, number_of_shares, fee) for each sale transaction.
        :return: The average stock price after all transactions including fees.
        """
        # Calculate the total value and number of shares based on purchase transactions
        total_purchase_value = sum((price * quantity + fee)
                                for price, quantity, fee in buy_transactions)
        total_shares = sum(quantity for _, quantity, _ in buy_transactions)

        if sell_transactions:
            # Update the number of shares and average price after sale transactions
            for sale_price, sell_quantity, sell_fee in sell_transactions:
                # Assume that shares are sold in the order they were purchased (FIFO)
                while sell_quantity > 0 and total_shares > 0:
                    # Get the oldest purchase transaction
                    purchase_price, purchased_quantity, _ = buy_transactions[0]

                    if purchased_quantity <= sell_quantity:
                        total_purchase_value -= purchased_quantity * purchase_price
                        total_purchase_value += sell_fee
                        total_shares -= purchased_quantity
                        sell_quantity -= purchased_quantity
                        buy_transactions.pop(0)
                    elif purchased_quantity == sell_quantity:
                        total_purchase_value -= sell_quantity * purchase_price
                        total_purchase_value += sell_fee
                        total_shares -= sell_quantity
                        buy_transactions[0] = (
                            purchase_price, purchased_quantity - sell_quantity)
                        sell_quantity = 0
                    elif purchased_quantity > sell_quantity:
                        total_purchase_value -= sell_quantity * purchase_price
                        total_purchase_value += sell_fee
                        total_shares -= sell_quantity
                        sell_quantity = 0

        # Calculate the average price after all transactions
        if total_shares > 0:
            average_price = total_purchase_value / total_shares
        else:
            average_price = 0
            # TODO: Może jakaś obsługa, żeby przy kalejnych zakupach nie musieć tego wszystkie liczyć
            # Gdy byłoby mnóstwo tranzakcji

        return average_price







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


   