from .views import (ProductViewSet, 
                    ProductSoftDelete)
from django.urls import path, include

urlpatterns = [
    path("product/", ProductViewSet.as_view()),
    path("product-delete/<int:pk>/", ProductSoftDelete.as_view()),
]