from django.shortcuts import render
from rest_framework import generics, viewsets

from authentication.models import UserProfile
from .serializers import UserSerializer, OperationSerializer, AssetAllocationSerializer, PocketSerializer, CurencySerializer, AssetClassSerializer
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .models import Operation, AssetAllocation, Pocket, Currency, AssetClass

from .lib.asset_processor import process_operation, update_assets

class UsersView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
class UserRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    

class OperationsViewSet(viewsets.ModelViewSet):
    serializer_class = OperationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Operation.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):

        serializer.save(owner=self.request.user)
        process_operation(data = serializer.data, owner = self.request.user)


class PocketsViewSet(viewsets.ModelViewSet):
    serializer_class = PocketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pocket.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AssetAllocationViewSet(viewsets.ModelViewSet):
    serializer_class = AssetAllocationSerializer
    permission_classes = [IsAuthenticated]
    # get_queryset = AssetAllocation.objects.all()
    
    def get_queryset(self):
        pocket_name = self.request.query_params.get('pocket_name', None)
        pocket = Pocket.objects.get(owner = self.request.user, name = pocket_name)
        update_assets(pocket_name=pocket_name, owner=self.request.user)

        return AssetAllocation.objects.filter(pocket=pocket)
    
class CurencyViewSet(viewsets.ModelViewSet):
    serializer_class = CurencySerializer
    permission_classes = [IsAuthenticated]
    queryset = Currency.objects.all()

class AssetClassViewSet(viewsets.ModelViewSet):
    serializer_class = AssetClassSerializer
    permission_classes = [IsAuthenticated]
    queryset = AssetClass.objects.all()