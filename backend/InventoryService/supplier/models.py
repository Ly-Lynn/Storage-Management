from django.db import models

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    logo = models.ImageField(upload_to='supplier_logos/')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class SupplierProduct(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    price_import = models.DecimalField(max_digits=10, decimal_places=2)
    total_quantity = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    last_stock_date = models.DateTimeField()
    def __str__(self):
        return f"{self.product_id} - {self.price} - {self.stock}"