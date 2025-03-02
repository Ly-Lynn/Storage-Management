from celery import shared_task, current_app
from django.conf import settings
from datetime import datetime, timedelta, timezone
from django.utils import timezone
from .models import (
    StockMovement
)

@shared_task(name="stock_movement.delete_stock")
def delete_stock(stock_id):
    obj = StockMovement.objects.get(id=stock_id)
    obj.is_deleted = True
    obj.last_updated = timezone.now()
    obj.save()
    return f"\n✅ Stock Movement {stock_id} deleted successfully.\n"
@shared_task(name="stock_movement.delete_expired")
def delete_expired():
    expired_stock_movements = StockMovement.objects.filter(last_updated__lte=datetime.now() - timedelta(days=365))
    count = expired_stock_movements.count()
    expired_stock_movements.delete()
    print(f"\n✅ Deleted {count} expired stock movements.\n")