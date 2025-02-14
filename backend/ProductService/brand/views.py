from django.shortcuts import render
from .serializers import BrandSerializers
from .models import ProductBrand
from rest_framework import viewsets
# Create your views here.
class BrandViews(viewsets.ModelViewSet):
    queryset = ProductBrand.objects.all()
    serializer_class = BrandSerializers
    ordering_fields = ['name']
    search_fields = ['name']