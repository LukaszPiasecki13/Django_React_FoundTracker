from rest_framework import serializers
from authentication.models import UserProfile
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
    
class OperationSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = models.Operation
        fields = "__all__"

class AssetAllocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AssetAllocation
        fields = "__all__"
        depth = 2

class PocketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pocket
        fields = "__all__"

class CurencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = "__all__"

class AssetClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssetClass
        fields = "__all__"
