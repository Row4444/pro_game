import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class TaskStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope[
            "user"
        ]  # from middleware pro_game.middleware.TokenAuthMiddleware
        self.task_id = self.scope["url_route"]["kwargs"]["task_id"]
        self.group_name = f"task_{self.task_id}"

        if (
            self.user.is_anonymous or not self.task_exists()
        ):  # verify if user have access for the task
            await self.close()
        else:
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    @database_sync_to_async
    def task_exists(self):
        """ check user has accept for this task """
        return self.user.task_set.filter(id=self.task_id).exists()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        status = text_data_json.get("status")

        await self.channel_layer.group_send(
            self.group_name, {"type": "task_status_update", "status": status}
        )

    async def task_status_update(
        self, event
    ):  # use in task.signals.send_task_status_update
        status = event["status"]
        await self.send(text_data=json.dumps({"status": status}))
