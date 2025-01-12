from django.urls import re_path
from task import consumers as task_consumers

websocket_urlpatterns = [
    re_path(
        r"ws/task-status/(?P<task_id>\d+)/$",
        task_consumers.TaskStatusConsumer.as_asgi(),
    ),
]
