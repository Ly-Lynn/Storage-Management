import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "InventoryService.settings")

app = Celery("InventoryService")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

from celery.schedules import crontab

app.conf.beat_schedule = {
    "delete-expired-inventories-every-24-hours": {
        "task": "inventory.delete_expired",
        "schedule": crontab(hour="*/24"), 
    },
    "delete-expired-suppliers-every-24-hours": {
        "task": "supplier.delete_expired",
        "schedule": crontab(hour="*/24"), 
    },
    "delete-expired-stock-every-24-hours": {
        "task": "stock_movement.delete_expired",
        "schedule": crontab(0, 0, day_of_month='1'), 
    },
}
