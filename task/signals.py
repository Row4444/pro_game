from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Task


@receiver(post_save, sender=Task)
def send_task_status_update(
    sender, instance, **kwargs
):  # for send message with websocket
    channel_layer = get_channel_layer()
    group_name = f"task_{instance.id}"

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "task_status_update",
            "status": instance.status,
        },
    )
