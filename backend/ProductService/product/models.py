from django.db import models

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.FloatField()
    description=models.TextField(max_length=500, null=True, blank=True, default="")
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE)
    brand = models.ForeignKey('brand.ProductBrand', on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_deleted=models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    def __str__(self):
        return self.name
    
