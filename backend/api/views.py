from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.views import APIView

from authentication.models import UserProfile
from .serializers import UserSerializer, OperationSerializer, AssetAllocationSerializer, PocketSerializer, CurencySerializer, AssetClassSerializer
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .models import Operation, AssetAllocation, Pocket, Currency, AssetClass
from rest_framework import status
from rest_framework.response import Response
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

from .lib.AssetProcessor import AssetProcessor

class UsersView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
class UserRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    

class OperationsViewSet(viewsets.ModelViewSet):
    serializer_class = OperationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pocket_name = self.request.query_params.get('pocket_name', None)
        queryset = Operation.objects.filter(owner=self.request.user, pocket_name=pocket_name)
        return queryset

    def perform_create(self, serializer):
        # TODO: Walidacja danych
        processor = AssetProcessor(data=serializer.validated_data, owner=self.request.user)
        try:
            if serializer.validated_data['operation_type'] == 'buy':
                result = processor.buy_operation()
            elif serializer.validated_data['operation_type'] == 'sell':
                result = processor.subtract_objects()
            elif serializer.validated_data['operation_type'] == 'add_funds':
                result = processor.add_funds()
            elif serializer.validated_data['operation_type'] == 'withdraw_funds':
                result = processor.withdraw_funds()
                
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})
        
        if result:
            serializer.save(owner=self.request.user)
        else:
            return Response({"error": "Error with operation processing"}, status=status.HTTP_400_BAD_REQUEST)


class PocketsViewSet(viewsets.ModelViewSet):
    serializer_class = PocketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = Pocket.objects.filter(owner=self.request.user)
        name = self.request.query_params.get('name', None)

        if name is not None:
            # Filter by name
            queryset = queryset.filter(name=name)
        
        return queryset


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AssetAllocationViewSet(viewsets.ModelViewSet):
    serializer_class = AssetAllocationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        pocket_name = self.request.query_params.get('pocket_name', None)
        processor = AssetProcessor(owner = self.request.user)
        processor.update_assets(pocket_name=pocket_name)
        pocket = Pocket.objects.get(name = pocket_name)

        return AssetAllocation.objects.filter(pocket=pocket)
    
class CurencyViewSet(viewsets.ModelViewSet):
    serializer_class = CurencySerializer
    permission_classes = [IsAuthenticated]
    queryset = Currency.objects.all()

class AssetClassViewSet(viewsets.ModelViewSet):
    serializer_class = AssetClassSerializer
    permission_classes = [IsAuthenticated]
    queryset = AssetClass.objects.all()

class ProfitDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pocket_name = request.query_params.get('pocketName')
        start_date_str = request.query_params.get('startDate')
        end_date_str = request.query_params.get('endDate')
        interval = "day"

        # start_date = end_date - timedelta(days=365)
        
        # try:
        #     start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        #     end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        # except ValueError:
        #     return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # if start_date > end_date:
        #     return Response({"error": "Start date cannot be after end date."}, status=status.HTTP_400_BAD_REQUEST)

        if pocket_name :
            operations = Operation.objects.filter(owner=request.user, pocket_name=pocket_name)
        else:
            operations = Operation.objects.filter(owner=request.user)
        
        portfolio_profit = pd.Series()

        for operation in operations:
            ticker = operation.ticker
            currrent_date = datetime.now()  

            ticker_data = yf.Ticker(ticker).history(start=operation.date, end=currrent_date)[['Close']]
            ticker_value = pd.Series(ticker_data['Close'].values, index=ticker_data.index)

            # We calculate the profit for a given ticker
            ticker_value = (ticker_value*operation.quantity-operation.fee - operation.price*operation.quantity).round(2)
            portfolio_profit = portfolio_profit.add(ticker_value, fill_value=0)

        portfolio_profit = portfolio_profit.round(2)
        portfolio_profit_reset = portfolio_profit.reset_index()
        portfolio_profit_reset.columns = ['Date', 'Close']
        # print(portfolio_profit_reset)

        if interval == "day":
            portfolio_profit_reset['Date'] = portfolio_profit_reset['Date'].dt.strftime('%Y-%m-%d')

        return Response(portfolio_profit_reset, status=status.HTTP_200_OK)
