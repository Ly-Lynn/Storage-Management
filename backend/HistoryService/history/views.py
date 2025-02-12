from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import HistorySerializer
from .models import History
from .tasks import rollback_history_tasks, create_history
# Create your views here.
class HistoryViewSet(generics.ListCreateAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HistoryRollback(generics.CreateAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        his_id = instance.id
        action = "ROLLBACK"
        value_before = instance.value_after
        value_after = instance.value_before
        created_at = datetime.now()
        name_field_updated = instance.name_field_updated
        service_updated = instance.service_updated
        object_id = instance.object_id
        endpoint = instance.endpoint
        data = {
            "action": action,
            "value_before": value_before,
            "value_after": value_after,
            "created_at": created_at,
            "name_field_updated": name_field_updated,
            "service_updated": service_updated,
            "object_id": object_id,
            "endpoint": endpoint
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            instance.delete()
            create_history.delay(data)
            rollback_history_tasks.delay(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)