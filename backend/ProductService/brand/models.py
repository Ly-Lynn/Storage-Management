from django.db import models

# Create your models here.
class ProductBrand(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(max_length=500, null=True, blank=True, default="")
    link_web = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name