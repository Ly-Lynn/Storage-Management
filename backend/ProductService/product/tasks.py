from celery import shared_task, current_app 
import requests
import redis
from django.conf import settings
from .models import (
    Product
)
redis_client = redis.StrictRedis(host=settings.REDIS_HOST, 
                                 port=settings.REDIS_PORT, 
                                 db=settings.REDIS_DB,)


@shared_task(name="product.create_history")   
def create_history(data):
    result = current_app.send_task("history.create_history", args=[data])
    if result:
        return f"\n✅ Product history created successfully.\n"
    return f"\n❌ Failed to create product history.\n"

@shared_task(name="product.delete_product")
def soft_delete_product(product_id):
    supplier_product_res = current_app.send_task("supplier.delete_product", args=[product_id])
    inven_res = current_app.send_task("inventory.delete_product", args=[product_id])
    if supplier_product_res and inven_res:
        product = Product.objects.get(id=product_id)
        product.is_deleted = True
        product.save()
        return f"\n✅ Product {product_id} deleted successfully.\n"
    return f"\n❌ Failed to delete product {product_id}.\n"

@shared_task(name="product.rollback_task")
def rollback_task(object_id, payload):
    name_fields = payload.get("name_field_updated")
    value_after = payload.get("value_after")
    obj = Product.objects.get(id=object_id)
    for field in name_fields:
        setattr(obj, field, value_after.get(field))
    obj.save()
    return f"\n✅ Product {object_id} rolled back successfully.\n"
    