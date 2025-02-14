from django.db import models

# Create your models here.
class Inventory(models.Model):
    product_id = models.IntegerField()
    stock = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    is_deleted=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.product_id} - {self.stock}"