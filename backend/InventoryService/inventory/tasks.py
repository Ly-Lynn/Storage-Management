from celery import shared_task, current_app
from django.conf import settings
from datetime import datetime, timedelta, timezone
from django.utils import timezone
from .models import (
    Inventory
)

@shared_task(name="inventory.create_inventory")
def create_update_inventory(data):
    inventory_data = {
        "product_id": data['product_id'],
        "stock": data['stock'],
        "last_updated": timezone.now()
    }
    if data['method'] == "update":
        obj = Inventory.objects.get(product_id=data['product_id'])
        obj.stock = data['stock']
        obj.last_updated = timezone.now()
        obj.save()
        return "\n✅ Inventory updated successfully.\n"
    if data['method'] == "create":
        Inventory.objects.create(**inventory_data)
    
    return "\n✅ Inventory created successfully.\n"

@shared_task(name="inventory.delete_product")
def delete_product(product_id):
    obj = Inventory.objects.get(product_id=product_id)
    obj.is_deleted = True
    obj.last_updated = timezone.now()
    obj.save()
    return f"\n✅ Inventory of {product_id} deleted successfully.\n"

@shared_task(name="inventory.delete_expired")
def delete_expired():
    expired_inventories = Inventory.objects.filter(last_updated__lte=datetime.now() - timedelta(days=30))
    count = expired_inventories.count()
    expired_inventories.delete()
    print(f"\n✅ Deleted {count} expired inventories.\n")
