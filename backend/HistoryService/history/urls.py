from django.urls import path, include

from .views import (HistoryViewSet,
                    HistoryRollback)

urlpatterns = [
    path("history/", HistoryViewSet.as_view()),
    path("history-redo/<int:pk>/", HistoryRollback.as_view()),
]