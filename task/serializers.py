from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]

    def validate_description(self, value):
        """ Do not create blank lines in Task.description"""
        if isinstance(value, str) and not value.strip():
            return None
        return value