from celery import shared_task, current_app
from datetime import timedelta, datetime
from .models import History

@shared_task(name="history.create_history")
def create_history(data):
    """
    data = {
        "instance": instance,
        "request": request:Dict {name_field_updated: value_after},
        "service_updated": service_updated,
        "action": action,
        "
    }
    """
    instance = data.get('instance')
    fields_updated = set(data.get('request').data.keys())
    value_before = {
        field: getattr(instance, field) 
        for field in fields_updated
        if hasattr(instance, field)
    }
    his_data = {
        "object_id": instance.id,
        "service_updated": data.get('service_updated'),
        "name_fields_updated": list(fields_updated),
        "value_before": value_before,
        "value_after": data.get('request'),
        "action": data.get('action'),
        "user_id": data.get('user_id')
    }
    History.objects.create(**his_data)
    return "\n✅ History created successfully.\n"

@shared_task(name="history.delete_expired_history")
def delete_expired_history():
    expired_histories = History.objects.filter(date_created__lte=datetime.now() - timedelta(days=365))
    count = expired_histories.count()
    expired_histories.delete()
    print(f"\n✅ Deleted {count} expired histories.\n")

@shared_task(name="history.rollback_history_tasks")
def rollback_history_tasks(data):
    value_after = data.get('value_after')
    name_field_updated = data.get('name_field_updated')
    service_updated = data.get('service_updated')
    object_id = data.get('object_id')
    # endpoint = data.get('endpoint')
    
    # data needs to be rolled back
    payload = {"name_field_updated": name_field_updated, "value_after": value_after}
    if service_updated == "ProductService":
        result = current_app.send_task("product.rollback_task", args=[object_id, payload])
    elif service_updated == "InventoryService":
        result = current_app.send_task("inventory.rollback_task", args=[object_id, payload])
    else:
        return "\n❌ Unknown service to rollback.\n"
    
    return f"\n✅ Rollback task dispatched via RabbitMQ successfully. Task ID: {result.id}\n"
