from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import (
    Inventory
)
from .serializers import (
    InventorySerializer
)

# Inventory only show information related to stock of products {id}
#  => has only Retrieve and List API
# cannot update, soft delete only happend when product is deleted
class InventoryView(generics.RetrieveAPIView, generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer  
    ordering_fields = ['stock']
    search_fields = ['product_id']
    
    