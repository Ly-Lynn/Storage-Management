from django.shortcuts import render
from datetime import datetime
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
import requests
from django.conf import settings

from .serializers import (
    ProductSerializer
)
from .models import (
    Product
)
from .tasks import (update_stock, 
                    create_inventory, 
                    create_history, 
                    soft_delete_product)

# Create your views here.
class ProductViewSet(generics.ListCreateAPIView, generics.RetrieveUpdateAPIView):
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer
    ordering_fields = ['price', 'quantity']
    search_fields = ['name', 'category__name', 'brand__name']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            inventory_obj = {
                'product_id': serializer.data.get('id'),
                'quantity': serializer.data.get('quantity'),
                'supplier': serializer.data.get('supplier'),
                'last_updated': serializer.data.get('updated_at')
            }
            history_obj = {
                "action": "CREATE",
                "value_before": None,
                "value_after": serializer.data.get("value"),
                "created_at": datetime.now(),
                "name_field_updated": serializer.data.get('name_field'),
                # "user": request.user,
                "service_updated": "ProductService",
                "object_id": serializer.data.get('id'),
                "endpoint": "products"
            }
            create_history.delay(history_obj)
            response = requests.post(settings.INVENTORY_SERVICE_URL , json=inventory_obj)
            
            # need response immediately to return notification to user  
            if response.status_code != 201: 
                return Response({'error': 'Inventory creation failed'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        value_before = Product.objects.get(id=serializer.data.get('id')).value
        if serializer.is_valid():
            serializer.save()
            history_obj = {
                "action": "UPDATE",
                "value_before": value_before,
                "value_after": serializer.data.get("value"),
                "created_at": datetime.now(),
                "name_field_updated": serializer.data.get('name_field'),
                # "user": request.user,
                "service_updated": "ProductService",
                "object_id": serializer.data.get('id'),
                "endpoint": "products"
            }

class ProductSoftDelete(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        data = {
            "action": "DELETE",
            "value_before": False,
            "value_after": True,
            "created_at": datetime.now(),
            "name_field_updated": "is_deleted",
            # "user": request.user,
            "service_updated": "ProductService",
            "object_id": instance.id,
            "endpoint": "products"
        }
        create_history.delay(data)
        return Response({
            "message": "Product deleted successfully",
        }, status=status.HTTP_200_OK)
    