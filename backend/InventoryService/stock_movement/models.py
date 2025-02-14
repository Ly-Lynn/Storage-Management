from django.db import models
from InventoryService import supplier
# Create your models here.
class StockMovement(models.Model):
    product_id = models.IntegerField()
    supplier = models.ForeignKey(supplier.Supplier, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    movement_type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.product_id} - {self.quantity} - {self.movement_type}"