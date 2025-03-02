from django.db import models
from InventoryService.supplier.models import Supplier
# Create your models here.
class StockMovement(models.Model):
    product_id = models.IntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    move_type = models.Choices(
        ('IN', 'IN'),
        ('OUT', 'OUT')
    )
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    movement_type = models.CharField(max_length=20)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.product_id} - {self.quantity} - {self.movement_type}"