from rest_framework import serializers
from authentication.models import UserProfile
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
    
class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Operation
        fields = "__all__"

class AssetAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssetAllocation
        fields = "__all__"

class PocketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pocket
        fields = "__all__"
