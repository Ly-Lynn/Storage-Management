from celery import shared_task, current_app
from django.conf import settings
from django.utils import timezone
from .models import (
    Supplier,
    SupplierProduct
)
@shared_task(name="supplier.create_history")
def create_history(data):
    result = current_app.send_task("history.create_history", args=[data])
    if result:
        return f"\n✅ History created successfully.\n"
    return f"\n❌ Failed to create history.\n"

@shared_task(name="supplier.delete_product")
def delete_product(product_id):
    obj = SupplierProduct.objects.get(product_id=product_id)
    obj.is_deleted = True
    obj.last_updated = timezone.now()
    obj.save()
    return f"\n✅ Supplier-Product {product_id} deleted successfully.\n"
 
@shared_task(name="supplier.delete_expired")
def delete_expired():
    expired_supplier_products = SupplierProduct.objects.filter(last_updated__lte=timezone.now() - timedelta(days=30))
    count = expired_supplier_products.count()
    expired_supplier_products.delete()
    print(f"\n✅ Deleted {count} expired supplier products.\n")

@shared_task(name="supplier_product.create")
def create_supplier_product(data):
    supplier_product_data = {
        "supplier": data['supplier'],
        "product_id": data['product_id'],
        "price_import": data['price_import'],
        "total_quantity": data['total_quantity'],
        "last_stock_da"
        "last_updated": timezone.now()
    }
    SupplierProduct.objects.create(**supplier_product_data)
    return "\n✅ Supplier-Product created successfully.\n"