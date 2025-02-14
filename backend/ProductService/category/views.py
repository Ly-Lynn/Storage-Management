from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import (
    Category
)
from .serializers import CategorySerializer
# Create your views here.

class CategoryViews(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    ordering_fields = ['name']
    search_fields = ['name']


