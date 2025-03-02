from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from .models import (
    Supplier,
    SupplierProduct
)

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        extra_kwargs = {
            "name": {
                "validators": [
                    UniqueValidator(queryset=Supplier.objects.all())
                ]
            },
        }
    
class SupplierProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierProduct
        fields = '__all__'
        extra_kwargs = {
            "supplier": {
                "validators": [
                    UniqueTogetherValidator(queryset=SupplierProduct.objects.all(), fields=['supplier', 'product_id'])
                ]
            },
        }
