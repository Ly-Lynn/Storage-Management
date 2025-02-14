import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HistoryService.settings")

app = Celery("HistoryService")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

from celery.schedules import crontab

app.conf.beat_schedule = {
    "delete-history-more-than-1-year": {
        "task": "history.tasks.delete_expired_history",
        "schedule": crontab(month_of_year="*/1"),  
    },
}