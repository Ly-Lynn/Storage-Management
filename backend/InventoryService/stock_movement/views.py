from django.shortcuts import render
from celery import current_app
from .models import StockMovement
from InventoryService.supplier.models import (
    Supplier,
    SupplierProduct
)
from .serializers import StockMovementSerializer
from rest_framework import viewsets, generics
from django.utils import timezone

# Create your views here.
class StockMovementList(generics.ListCreateAPIView):
    queryset = StockMovement.objects.all(is_deleted=False)
    serializer_class = StockMovementSerializer
    def create(self, request, *args, **kwargs):
        supplier = Supplier.objects.get(id=request.data['supplier'])
        supplier_product = SupplierProduct.objects.get(product_id=request.data['product_id'], supplier=supplier)
        if not supplier_product:
            supplier_product_data = {
                "supplier": supplier,
                "product_id": request.data['product_id'],
                "price_import": request.data['price_per_unit'],
                "total_quantity": request.data['quantity'],
                "last_updated": timezone.now(),
                "last_stock_date": timezone.now()
            }    
            SupplierProduct.objects.create(**supplier_product_data)
        else:
            supplier_product.price_import = request.data['price_per_unit']
            supplier_product.total_quantity += request.data['quantity']
            supplier_product.last_updated = timezone.now()
            supplier_product.last_stock_date = timezone.now()
            supplier_product.save()
        response = super().create(request, *args, **kwargs)
        return response

class StockMovementDetail(generics.RetrieveUpdateAPIView):
    queryset = StockMovement.objects.all(is_deleted=False)
    serializer_class = StockMovementSerializer