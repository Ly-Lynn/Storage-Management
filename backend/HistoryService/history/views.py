from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from bson import ObjectId

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
    serializer_class = HistorySerializer

    def create(self, request, *args, **kwargs):
        history_id = self.kwargs.get("pk")

        try:
            if not ObjectId.is_valid(history_id):
                return Response({"error": "Invalid ObjectId"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "ObjectId error"}, status=status.HTTP_400_BAD_REQUEST)

        instance = History.objects.filter(id=history_id).first()
        if not instance:
            return Response({"error": "History not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "action": "ROLLBACK",
            "value_before": instance.value_after,
            "value_after": instance.value_before,
            "created_at": timezone.now(),
            "name_field_updated": instance.name_field_updated,
            "service_updated": instance.service_updated,
            "object_id": instance.object_id,
            "endpoint": instance.endpoint,
        }

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        create_history.delay(data)  
        rollback_history_tasks.delay(data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)