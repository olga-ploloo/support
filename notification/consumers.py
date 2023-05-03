import json

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer

from notification.models import Notification


@database_sync_to_async
def create_notification(receiver, typeof="ticket_created", status="unread"):
    notification_to_create = Notification.objects.create(user_revoker=receiver, type_of_notification=typeof)
    return (notification_to_create.user_receiver.username, notification_to_create.type_of_notification)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        print('Am i finallyy here')
        print(self.scope['user'].id)
        await self.accept()
        await self.send(json.dumps({
            "type": "websocket.send",
            "text": "hello world"
        }))
