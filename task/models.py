from django.contrib.auth.models import User
from django.db import models

from utils.enum import ChoicesEnum


class StatusEnum(ChoicesEnum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class PriorityEnum(ChoicesEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)  # Do not use in filters, but in general, index needed
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=StatusEnum.choices(),
        default=StatusEnum.NEW.value,
        db_index=True,  # bad practice for choices, but use in filters
    )
    priority = models.CharField(
        max_length=20,
        choices=PriorityEnum.choices(),
        default=PriorityEnum.MEDIUM.value,
        db_index=True,  # bad practice for choices, but use in filters
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
