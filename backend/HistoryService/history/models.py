from django.db import models
from djongo import models
# Create your models here.

class History(models.Model):
    object_id = models.CharField(max_length=255)  
    service_updated = models.CharField(max_length=255)
    name_field_updated = models.CharField(max_length=255)
    value_before = models.JSONField()  
    value_after = models.JSONField()
    action = models.CharField(max_length=50, default="UPDATE")
    endpoint = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.action} on {self.name_field_updated}: {self.value_before} -> {self.value_after} at {self.created_at}"