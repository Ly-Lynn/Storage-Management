from django.db import models

# Create your models here.
class History(models.Model):
    action = models.CharField(max_length=200)
    value_before = models.CharField(max_length=200)
    value_after = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    name_field_updated = models.CharField(max_length=200)
    object_id = models.IntegerField()
    endpoint = models.CharField(max_length=200)
    # user = models.CharField(max_length=200)
    service_updated = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.action} on {self.name_field_updated}: {self.value_before} -> {self.value_after} at {self.created_at}"