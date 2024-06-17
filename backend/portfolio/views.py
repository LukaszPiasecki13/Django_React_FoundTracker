from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.core.paginator import Paginator
from .models import AssetClass, Currency, Operation, Pocket, Asset, AssetAllocation
from django.contrib import messages
from .lib.asset_processor import add_objects, update_assets, delete_asset, subtract_assets
import traceback

import logging


logger = logging.getLogger(__name__)


@method_decorator(login_required(login_url='/authentication/login'), name='get')
class MainDashboardView(View):
    def get(self, request):
        context = {
            'pockets': Pocket.objects.filter(owner=request.user)
            
        }
        return render(request, "portfolio/main_dashboard.html")

    # def post(self, request):

    #     return render(request, "portfolio/main_dashboard.html")


@method_decorator(login_required(login_url='/authentication/login'), name='get')
class PocketView(View):

    def update_data(self, request) -> dict:

        if (request.GET.get('pocket_name') == None):
            pocket_name = request.session['pocket_name']
        else:
            pocket_name = request.GET.get('pocket_name')
            request.session['pocket_name'] = pocket_name

        update_assets(pocket_name = pocket_name, owner = request.user)

        asset_classes = AssetClass.objects.all()
        currencies = Currency.objects.all() 
        pocket = Pocket.objects.get(name = pocket_name, owner = request.user)
        asset_allocations = AssetAllocation.objects.filter(pocket = pocket)

        # Get used asset classes

        used_asset_classes_dict = {}
        for asset_allocation in asset_allocations:
            if asset_allocation.asset.asset_class not in used_asset_classes_dict:
                used_asset_classes_dict[asset_allocation.asset.asset_class] = [asset_allocation.asset.ticker]
            else:
                used_asset_classes_dict[asset_allocation.asset.asset_class].append(asset_allocation.asset.ticker)
        

        paginator = Paginator(asset_allocations, 10)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)

        context = {
            'asset_classes': asset_classes,
            'currencies': currencies,
            'pocket_name': pocket_name,
            'asset_allocations': asset_allocations,
            'used_asset_classes_dict': used_asset_classes_dict,
            'page_obj': page_obj
            
        }

        return context

    def get(self, request):
        context = self.update_data(request)
        return render(request, "portfolio/pocket.html", context)

    def post(self, request):

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
            'owner': request.user,
            'pocket_name': request.session['pocket_name']
        }

        if data['fee'] == '':
            data['fee'] = '0'

        # OPERATION
        # Create operation object
        operation = Operation.objects.create(
            operation_type=data['operation_type'],
            asset_class=data['asset_class'],
            ticker=data['ticker'],
            date=data['date'],
            currency= data['currency'],
            quantity=data['quantity'],
            price=data['price'],
            fee=data['fee'],
            comment=data['comment'],
            owner=data['owner'],
            pocket_name=data['pocket_name']
        )

        try:
            if data['operation_type'] == 'buy':
                try:
                    _ = add_objects(data)
                    messages.success(request, "Purchase added successfully")
                
                except Exception as error:
                        logger.error("Purchase added error: {}".format(error))
                        logger.error(traceback.format_exc()) 

                        if error.args[0] == 'longName':
                            messages.error(request, "Purchase added error: Asset not found in Yahoo Finance")
                        else:
                            messages.error(request, "Purchase added error: {}".format(error))

                        raise Exception("Purchase added error: {}".format(error))
                        
            elif data['operation_type'] == 'sell':
                try:
                    _ = subtract_assets(pocket_name = data['pocket_name'], 
                                        owner = data['owner'], 
                                        quantity = data['quantity'], 
                                        ticker = data['ticker'],
                                        fee = data['fee'])
                    ...
                except Exception as error:
                    logger.error("Sell added error: {}".format(error))
                    logger.error(traceback.format_exc()) 
                    messages.error(request, "Sell added error: {}".format(error))    

                    raise Exception("Sell added error: {}".format(error))    

        except Exception as error:
            operation.delete()

        context = self.update_data(request)

        return render(request, "portfolio/pocket.html", context)


@method_decorator(login_required(login_url='/authentication/login'), name='get')
class PocketHistoryView(View):
    def get(self, request):
        operations = Operation.objects.filter(owner=request.user)
        paginator = Paginator(operations, 10)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)
        context = {
            'operations': operations,
            'pocket_name': request.session['pocket_name'],
            'page_obj': page_obj
        }
        return render(request, "portfolio/pocket_history.html", context)
    
    def post(self, request):
        # TODO: W momencie gdy usuwam operację sell to inna operacja
        try:
            _ = delete_asset(id = request.POST['operation_id'])
        except Exception as error:
            logger.error("Operation delete error: {}".format(error))
            logger.error(traceback.format_exc()) 
            return False
        
        operations = Operation.objects.filter(owner=request.user)
        context = {
            'operations': operations,
            'pocket_name': request.session['pocket_name']
        }
        return render(request, "portfolio/pocket_history.html", context)
    

    