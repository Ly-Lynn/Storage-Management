from rest_framework import serializers
from .models import StockMovement

"""
{
    "product_id": 1,
    "quantity": 100,
    "supplier": 1,
    "price_per_unit": 1000,
    "move_type": "IN",
    }
"""

class StockMovementSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()
    price_per_unit = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_price = serializers.SerializerMethodField(method_name = 'get_total_price')
    move_type = serializers.ChoiceField(choices = ['IN', 'OUT'])
    class Meta:
        model = StockMovement
        fields = ['product_id', 'quantity', 'supplier', 'price_per_unit', 'total_price', 'move_type']
    def get_total_price(self, obj:StockMovement):
        return obj.quantity * obj.price_per_unit