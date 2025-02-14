from rest_framework import serializers
from django.conf import settings
import requests
from rest_framework import status
from .models import (
    Product
)
from category.models import (
    Category
)
from brand.models import (
    ProductBrand
)

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    image = serializers.CharField()
    brand_id = serializers.IntegerField(write_only=True)
    category_id = serializers.IntegerField(write_only=True)

    # for Inventory Service    
    
    quantity = serializers.IntegerField(write_only=True)
    
    # Serializer automatically process this field by methods
    # contain stock info and suppliers info
    inventory_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'image',
            'created_at', 'updated_at', 'inventory',
            'category_id', 'supplier', 'quantity'
        ]


    def get_all_stock(self):
        try:
            response = requests.get(f"{settings.INVENTORY_SERVICE_URL}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                inventory_data = data.get('inventory', {})
                supplier_data = data.get('supplier', {})
                stock = inventory_data.get(str(self.instance.id), 0)  # stock by product.id
                supplier = supplier_data.get(str(self.instance.id), 'N/A')  # supplier by product.id
                return {
                    'stock': stock,
                    'supplier': supplier, # supplier: list of supplier(s)
                    'status': status.HTTP_200_OK
                }
        except Exception as e:
            pass
        return {'status': status.HTTP_500_INTERNAL_SERVER_ERROR}

    def get_stock(self, obj):
        try:
            url = f"{settings.INVENTORY_SERVICE_URL}{obj.id}/"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'stock': data.get('stock', 0),
                    'supplier': data.get('supplier', 'N/A'),
                    'status': status.HTTP_200_OK
                }
        except Exception as e:
            pass
        return {'status': status.HTTP_500_INTERNAL_SERVER_ERROR}

    def save(self):
        cate = Category.objects.get(id=self.validated_data['category_id'])
        brand = ProductBrand.objects.get(id=self.validated_data['brand_id'])
        product = Product.objects.create(
            name=self.validated_data['name'],
            description=self.validated_data['description'],
            price=self.validated_data['price'],
            category=cate,
            brand=brand,
            image=self.validated_data['image']
        )
        return product