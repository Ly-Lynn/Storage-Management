from .views import StockMovementList, StockMovementDetail
from django.urls import path


urlpatterns = [
    path('inventory/stock/', StockMovementList.as_view(), name='stock_movement_list'),
    path('inventory/stock/<int:pk>/', StockMovementDetail.as_view(), name='stock_movement_detail'),
]