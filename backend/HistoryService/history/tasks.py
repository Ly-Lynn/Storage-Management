from celery import shared_task
import requests
import redis
from django.conf import settings
from datetime import timedelta, datetime

from .models import History

@shared_task
def create_history(data):
    History.objects.create(**data)
    return f"\n✅ History created successfully.\n"

@shared_task
def delete_expired_history():
    expired_histories = History.objects.filter(date_created__lte=datetime.now() - timedelta(days=365))
    count = expired_histories.count()
    expired_histories.delete()
    print(f"\n✅ Deleted {count} expired histories.\n")

@shared_task
def rollback_history_tasks(data):
    value_after = data.get('value_after')
    name_field_updated = data.get('name_field_updated')
    service_updated = data.get('service_updated')
    object_id = data.get('object_id')
    endpoint = data.get('endpoint')
    if service_updated == "ProductService":
        response = requests.put(f"{settings.PRODUCT_SERVICE_URL}{endpoint}/{object_id}/", 
                                json={"name_field_updated": name_field_updated,
                                      "value_after": value_after})
    elif service_updated == "InventoryService":
        response = requests.put(f"{settings.INVENTORY_SERVICE_URL}{endpoint}/{object_id}/", 
                                json={"name_field_updated": name_field_updated,
                                      "value_after": value_after})
    if response.status_code == 201:
        return f"\n✅ History rolled back successfully.\n"
    return f"\n❌ Failed to rollback history.\n"