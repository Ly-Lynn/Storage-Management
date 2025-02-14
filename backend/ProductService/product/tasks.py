from celery import shared_task
import requests
import redis
from django.conf import settings

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, 
                                 port=settings.REDIS_PORT, 
                                 db=settings.REDIS_DB,)

@shared_task
def update_stock(product_id, quantity): # Update stock when an order is placed
    lock_key = f"inventory_update_lock_{product_id}"
    lock = redis_client.lock(lock_key, timeout=7)  

    if not lock.acquire(blocking=False):
        return f"\nInventory for product {product_id} is being updated. Skipping update."

    try:
        inventory_obj = {
            "quantity": quantity
        }
        response = requests.put(f"{settings.INVENTORY_SERVICE_URL}{product_id}/", json=inventory_obj)

        if response.status_code == 200:
            return f"\nInventory updated for product {product_id}"
        return f"\nFailed to update inventory for product {product_id}"
    finally:
        lock.release()  

@shared_task    
def create_history(data):
    response = requests.post(f"{settings.HISTORY_SERVICE_URL}", json=data)
    if response.status_code == 201:
        return f"\n✅ History created successfully.\n"
    return f"\n❌ Failed to create history.\n"

@shared_task
def soft_delete_product(product_id):
    supplierproduct_response = requests.patch(f"{settings.INVENTORY_SERVICE_URL}supplier-product/{product_id}", 
                                                json={"is_deleted": True})
    inventory_response = requests.patch(f"{settings.INVENTORY_SERVICE_URL}{product_id}/", 
                                        json={"is_deleted": True})
    if supplierproduct_response.status_code == 204 and inventory_response.status_code == 204:
        return f"\n✅ Product {product_id} deleted successfully.\n"
    elif supplierproduct_response.status_code != 204:
        return f"\n❌ Failed to delete supplier product {product_id}.\n"
    elif inventory_response.status_code != 204:
        return f"\n❌ Failed to delete inventory of product {product_id}.\n"
