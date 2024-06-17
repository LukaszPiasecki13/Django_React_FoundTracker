from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Sum
from ..models import AssetClass, Currency, Operation, Pocket, Asset, AssetAllocation

from decimal import Decimal

import yfinance as yf





def add_objects(data: dict):
    '''
    Function that processes the data from the form and saves it to the database.
    :param data: dict
        data = {
            'operation_type': request.POST['operation'],
            'ticker': request.POST['ticker'],
            'date': request.POST['date'],
            'currency': request.POST['currency'],
            'quantity': request.POST['quantity'],
            'price': request.POST['price'],
            'fee': request.POST['fee'],
            'comment': request.POST['comment'],
            'asset_class': request.POST['asset_class'],
            'owner' : request.user,
            'pocket_name': request.session['pocket_name']
        }
    :return: bool, Exception

    '''

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
            currency=Currency.objects.get(name= data['currency']))

        if not asset_query.exists():
            Asset.objects.create(
                ticker=data['ticker'],
                name=asset_name,
                asset_class=data['asset_class'],
                currency=Currency.objects.get(name= data['currency']))

        # POCKET
        if data['fee'] != 0:
            pocket = Pocket.objects.get(name=data['pocket_name'], owner=data['owner'])
            pocket.fees += Decimal(data['fee'])
            pocket.save()

        # ASSET ALLOCATION
        # Check if asset allocation exists in the database
        asset_allocation_query = AssetAllocation.objects.filter(
            pocket=Pocket.objects.get(name=data['pocket_name'], owner=data['owner']),
            asset=Asset.objects.get(ticker=data['ticker']))

        if asset_allocation_query.exists():
            asset_allocation = asset_allocation_query.first()

            average_purchase_price = update_average_purchase_price(
                pocket_name = data['pocket_name'], 
                owner=data['owner'], ticker=data['ticker'])
            
            asset_allocation.average_purchase_price = Decimal(average_purchase_price)   
            
            asset_allocation.quantity += Decimal(data['quantity'])
            asset_allocation.save()
        else:

            AssetAllocation.objects.create(
                pocket=Pocket.objects.get(name=data['pocket_name'], owner=data['owner']),
                asset=Asset.objects.get(ticker=data['ticker']),
                quantity=data['quantity'],
                average_purchase_price=data['price']
            )
        
        return True
    
    except Exception as e:
        raise e


def subtract_assets(pocket_name, owner, quantity, ticker, fee):
    try:
        # POCKET
        if fee != 0:
            pocket = Pocket.objects.get(name=pocket_name, owner=owner)
            pocket.fees += Decimal(fee)
            pocket.save()

        # Modify asset_allocation object
        asset_allocation = AssetAllocation.objects.get(
            pocket=Pocket.objects.get(name=pocket_name, owner=owner),
            asset=Asset.objects.get(ticker=ticker))

        check_operation_indicator = asset_allocation.quantity-Decimal(quantity)
        if check_operation_indicator == 0:
            asset_allocation.delete()

            # Delete asset if quantity is 0
            Asset.objects.get(ticker=ticker).delete()

        elif check_operation_indicator > 0:
            asset_allocation.quantity -= Decimal(quantity)
            asset_allocation.save()
            ...
        elif check_operation_indicator < 0:
            raise ValueError("Quantity of asset cannot be negative")

        return True

    except Exception as e:
        raise e

def delete_asset(id):
    # TODO: Zrobić test na to
    try:
        operation = Operation.objects.get(id=id)

        if operation.operation_type == 'buy':
            if (subtract_assets(pocket_name = operation.pocket_name, 
                                owner=operation.owner, 
                                quantity=operation.quantity, 
                                ticker=operation.ticker,
                                fee=0)):
                operation.delete()
                return True
            else:
                raise ValueError("Something went wrong with deleting the asset")
        elif operation.operation_type == 'sell':
            if (add_objects(data = {
                        'ticker': operation.ticker,
                        'currency': operation.currency,
                        'quantity': operation.quantity,
                        'price': operation.price,
                        'currency': operation.currency,
                        'asset_class': operation.asset_class,
                        'owner': operation.owner,
                        'pocket_name': operation.pocket_name,
                        'fee': 0})):
                
                operation.delete()
                return True
            else:
                raise ValueError("Something went wrong with deleting the asset")    

    except Exception as e:
        raise e
    
def update_average_purchase_price(pocket_name, owner, ticker):
    buy_operations = Operation.objects.filter(
        owner=owner, 
        pocket_name=pocket_name,
        ticker=ticker,
        operation_type='buy')
    
    total_buy_value = 0
    total_quantity = 0

    for operation in buy_operations:
        total_buy_value += operation.quantity * operation.price
        total_quantity += operation.quantity
    
    average_purchase_price = total_buy_value / total_quantity
    return average_purchase_price


def update_assets(pocket_name, owner):
    
    asset_allocation_query = AssetAllocation.objects.filter(
        pocket=Pocket.objects.get(name=pocket_name, owner=owner))

    if asset_allocation_query.exists():
        total_value = 0

        for asset_allocation in asset_allocation_query:

            yf_info = yf.Ticker(asset_allocation.asset.ticker).info
            # Update the current price of the asset 
            asset_allocation.asset.current_price = Decimal(yf_info['currentPrice'])
            asset_allocation.asset.save()

            asset_allocation.daily_change_percent = (yf_info['currentPrice'] - yf_info['previousClose'])/yf_info['previousClose'] * 100
            asset_allocation.daily_change_XXX = Decimal((yf_info['currentPrice'] - yf_info['previousClose'])) *asset_allocation.quantity * asset_allocation.asset.currency.exchange_rate
            # TODO: Zrobić test na to
            # TODO: zrobić miejsce, gdzie będzie ustawiał siekurs wymiany

            asset_allocation.rate_of_return = (asset_allocation.asset.current_price - asset_allocation.average_purchase_price) / asset_allocation.average_purchase_price * 100
            asset_allocation.rate_of_return_XXX = asset_allocation.rate_of_return * asset_allocation.asset.currency.exchange_rate
            asset_allocation.profit_XXX = asset_allocation.rate_of_return_XXX * asset_allocation.quantity * asset_allocation.asset.current_price / 100
            # TODO: Zrobić test na to            
            asset_allocation.save()
            total_value += asset_allocation.quantity * asset_allocation.asset.current_price


        for asset_allocation in asset_allocation_query:
            asset_allocation.participation = asset_allocation.quantity * asset_allocation.asset.current_price / total_value * 100
             # TODO: Zrobić test na to   
            asset_allocation.save()
    else:

        ...
        

    ...

        

