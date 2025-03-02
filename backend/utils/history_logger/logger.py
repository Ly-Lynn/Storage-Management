# common_utils/history_logger/logger.py
from celery import current_app

def send_history_log(request, data):
    payload = {
        "object_id": data['object_id'],
        "service_updated": data['service_updated'],  
        "action": data['action'],
        # "endpoint": endpoint,
        "name_field_updated": data['name_field_updated'],
        "value_before": data['value_before'],
        "value_after": data['value_after'],
        "user_id": request.user.id if request.user else None,
    }
    # Gửi task đến History service qua RabbitMQ (Celery worker sẽ nhận task "history.create_history")
    current_app.send_task("history.create_history", args=[payload])
