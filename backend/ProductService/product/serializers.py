from rest_framework import serializers
from django.conf import settings
import requests
from rest_framework import status
from .models import (
    Product
)
class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    category = serializers.IntegerField()
    supplier = serializers.IntegerField()
    image = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    inventory = serializers.SerializerMethodField('get_inventory')

    class Meta:
        model = Product
        fields = '__all__'

    def get_inventory(self, obj):
        request = self.context.get("request")

        if request and request.parser_context.get("view").action == "list":
            return self.get_all_stock()
        return self.get_stock(obj)

    def get_all_stock(self):
        response = requests.get(settings.INVENTORY_SERVICE_URL + '/')
        if response.status_code == 200:
            return {
                'stock': response.json().get('stock', 0),
                'status': status.HTTP_200_OK    
            }
        return {
            'stock': 0,
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR
        }

    def get_stock(self, obj):
        response = requests.get(settings.INVENTORY_SERVICE_URL + f'/{obj.id}/')
        if response.status_code == 200:
            return {
                'stock': response.json().get('stock', 0),
                'status': status.HTTP_200_OK    
            }
        return {
            'stock': 0,
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    def save(self):
        product = Product.objects.create(
            name=self.validated_data['name'],
            description=self.validated_data['description'],
            price=self.validated_data['price'],
            category_id=self.validated_data['category'],
            image=self.validated_data['image']
        )
        return product