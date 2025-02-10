from django.db import models

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.FloatField(min_value=0)
    description=models.TextField(null=True, blank=True, default="")
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    def __str__(self):
        return self.name
    
