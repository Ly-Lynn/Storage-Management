import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ProductService.settings")

app = Celery("ProductService")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

from celery.schedules import crontab

# app.conf.beat_schedule = {
#     "check-otp-expiry-every-10-minutes": {
#         "task": "UserAPI.tasks.check_otp_expiry",
#         "schedule": crontab(minute="*/10"),  # Chạy mỗi 10 phút
#     },
#     "check-temp-user-every-5-minutes": {
#         "task": "UserAPI.tasks.delete_expired_temp_users",
#         "schedule": crontab(minute="*/10"),  # Chạy mỗi 10 phút
#     },
# }