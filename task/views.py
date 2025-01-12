from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    """list, create"""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    filterset_fields = {
        "created_at": ["gte", "gt", "lte", "lt"],
        "status": ["exact"],
        "priority": ["exact"],
    }

    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskGetUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """get, update, delete by id"""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
