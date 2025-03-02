from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from celery import current_app

from .models import Supplier, SupplierProduct
from .serializers import SupplierSerializer, SupplierProductSerializer
from .tasks import create_history

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.filter(is_deleted=False)
    serializer_class = SupplierSerializer

    def update(self, request, *args, **kwargs):
        instance = Supplier.objects.get(id=kwargs.get('pk'))
        if not instance:
            return Response(
                {"error": "Supplier not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        create_history.delay({
            "instance": instance,
            "request": request,
            "action": "PUT",
            "service_updated": "Inventory",
        })
        return super().update(request, *args, **kwargs)

    def partial_update(self, request,   *args, **kwargs):
        instance = Supplier.objects.get(id=kwargs.get('pk'))
        if not instance:
            return Response(
                {"error": "Supplier not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        create_history.delay({
            "instance": instance,
            "request": request,
            "action": "PATCH",
            "service_updated": "Inventory",
        })
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = Supplier.objects.get(id=kwargs.get('pk'))
            if not instance:
                return Response(
                    {"error": "Supplier not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            create_history.delay({
                "instance": instance,
                "request": request,
                "action": "DELETE",
                "service_updated": "Inventory",
            })
                
            instance.is_deleted = True
            instance.save()
            
            return Response(
                {"message": "Supplier deleted successfully"},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class SupplierProductViewSet(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = SupplierProduct.objects.filter(is_deleted=False)
    serializer_class = SupplierProductSerializer
    ordering_fields = ['price']
    search_fields = ['product_id']
    