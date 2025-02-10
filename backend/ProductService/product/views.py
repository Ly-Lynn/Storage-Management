from django.shortcuts import render
from datetime import datetime
from rest_framework import generics, viewsets, status
from rest_framework.response import Response

from .serializers import (
    ProductSerializer
)
from .models import (
    Product
)
from .tasks import create_product_inventory

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            inventory_obj = {
                'product_id': serializer.data.get('id'),
                'quantity': serializer.data.get('inventory').get('stock'),
                'supplier': serializer.data.get('supplier'),
                'last_updated': datetime.now()
            }
            create_product_inventory.delay(inventory_obj)
    
