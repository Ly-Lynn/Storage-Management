from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from .models import (
    Inventory
)

class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = ["product_id", "stock"]
        extra_kwargs = {
            'product_id': {
                'validators': [UniqueValidator(
                                queryset=Inventory.objects.all()
                                )]
            }
        }