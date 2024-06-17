from django.shortcuts import render
from rest_framework import generics, viewsets

from authentication.models import UserProfile
from .serializers import UserSerializer, OperationSerializer, AssetAllocationSerializer, PocketSerializer
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .models import Operation, AssetAllocation, Pocket

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
    

    def get_queryset(self):
        pocket = Pocket.objects.filter(owner = self.request.user)
        return AssetAllocation.objects.filter(pocket=pocket)