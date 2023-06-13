import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None

    async def connect(self):
        print("WebSocket Chat Connected!")
        user = self.scope['user']
        self.group_name = f'user_{user.id}'
        if user.is_authenticated:
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print("WebSocket Chat Disconnected!")

    async def notify(self, event):
        text_data = json.dumps({"message": event["message"]})
        await self.send(text_data)
