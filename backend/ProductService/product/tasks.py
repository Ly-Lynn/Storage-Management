from celery import shared_task
import requests
import random
from datetime import timedelta, datetime
from .models import (
    Product
)
from django.conf import settings

@shared_task
def create_product_inventory(inventory_obj):
    response = requests.post(settings.INVENTORY_SERVICE_URL + '/', json=inventory_obj)
    if response.status_code != 201:
        print(f"❌ Failed to create inventory for product {inventory_obj.get('product_id')}.")
    else:
        print(f"✅ Inventory created for product {inventory_obj.get('product_id')}.")