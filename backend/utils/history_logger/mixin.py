# common_utils/history_logger/mixin.py

class HistoryTrackingMixin:
    def create_history_data(self, request, instance, action):
        """
        Tạo payload history dựa trên instance đã cung cấp và request.
        :param request: HttpRequest contains data
        :param instance: instance had been retrieved from database
        :param action: (UPDATE, DELETE, CREATE, …)
        :return: history_data 
        """
        fields_updated = set(request.data.keys())
        
        value_before = {
            field: getattr(instance, field)
            for field in fields_updated
            if hasattr(instance, field)
        }
        
        history_data = {
            "object_id": instance.id,
            "service_updated": request.service_name,
            "name_fields_updated": list(fields_updated),
            "value_before": value_before,
            "value_after": request.data,
            "action": action,
            "user_id": request.user.id if request.user else None
        }
        
        return history_data
