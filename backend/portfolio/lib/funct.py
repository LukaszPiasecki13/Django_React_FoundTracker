from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from ..models import AssetClass, Currency, Operation, Pocket, Asset, AssetAllocation

import yfinance as yf





def process_asset_data(data: dict):
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

        # ASSET
        # Check if asset exists in the database
        asset_query = Asset.objects.filter(
            ticker=data['ticker'],
            name=asset_name,
            asset_class=data['asset_class'],
            currency=currency)

        if not asset_query.exists():
            Asset.objects.create(
                ticker=data['ticker'],
                name=asset_name,
                asset_class=data['asset_class'],
                currency=currency)

        # POCKET
        if data['fee'] != 0:
            pocket = Pocket.objects.get(name=data['pocket_name'], owner=data['owner'])
            pocket.fees += data['fee']
            pocket.save()

        # ASSET ALLOCATION
        # Check if asset allocation exists in the database
        asset_allocation_query = AssetAllocation.objects.filter(
            pocket=Pocket.objects.get(name=data['pocket_name'], owner=data['owner']),
            asset=Asset.objects.get(ticker=data['ticker']))

        if asset_allocation_query.exists():
            asset_allocation = asset_allocation_query.first()
            asset_allocation.quantity += data['quantity']
            asset_allocation.average_purchase_price = (asset_allocation.average_purchase_price * asset_allocation.quantity +
                                            data['price']) / (asset_allocation.quantity + data['quantity'])
            asset_allocation.save()
        else:
            AssetAllocation.objects.create(
                pocket=Pocket.objects.get(name=data['pocket_name'], owner=data['owner']),
                asset=Asset.objects.get(ticker=data['ticker']),
                quantity=data['quantity'],
                average_purchase_price=data['price']
            )
        
        return True, None
    
    except Exception as e:
        return False, e



if __name__ == "__main__":
    data = {
        'operation_type': 'Buy',
        'ticker': 'AAPL',
        'date': '2021-01-01',
        'currency': 'USD',
        'quantity': 10,
        'price': 100,
        'fee': 0,
        'comment': 'Bought 10 shares of AAPL',
        'asset_class': 'Stocks',
        'owner': 'user1',
        'pocket_name': 'Nazwa Konta1'
    }
