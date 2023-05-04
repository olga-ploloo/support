import json

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from notification.models import Notification


# @database_sync_to_async
# def create_notification(receiver, typeof="ticket_created", status="unread"):
#     notification_to_create = Notification.objects.create(user_revoker=receiver, type_of_notification=typeof)
#     return (notification_to_create.user_receiver.username, notification_to_create.type_of_notification)
#
#
# @database_sync_to_async
# def get_user(user_id):
#     try:
#         return get_user_model().objects.get(id=user_id)
#     except:
#         return AnonymousUser()


class TicketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Получите идентификатор билета из URL
        print('connection')
        self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']

        # Создайте группу каналов для данного билета
        await self.channel_layer.group_add(
            self.ticket_id,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Удалите соединение из группы каналов
        await self.channel_layer.group_discard(
            self.ticket_id,
            self.channel_name
        )

    async def receive(self, text_data):
        # Обработка входящих сообщений
        pass

    async def send_notification(self, event):
        print('sended')
        # Отправка уведомления в реальном времени
        notification = event['notification']

        # Отправить уведомление по WebSocket соединению
        await self.send(text_data=notification)

    #
    #     # Send message to WebSocket
    #     await self.send(text_data=json.dumps({"message": message}))

    #
    #
    # async def connect(self):
    #     self.group_name = 'notification'
    #     await self.channel_layer.group_add(self.group_name, self.channel_name)
    #     await self.accept()
    #
    #
    # async def disconnect(self, close_code):
    #     await self.channel_layer.group_discard(
    #         self.group_name,
    #         self.channel_name)
    # # вызывается когда метод получен из веб сокета
    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json["message"]
    #     event = {
    #         'type': 'send_message',
    #         'message': message
    #     }
    #
    #     await self.channel_layer.group_send(
    #         self.group_name,
    #         event)
    #
    # async def send_notification(self, event):
    #     message = event["message"]
    #
    #     # Send message to WebSocket
    #     await self.send(text_data=json.dumps({"message": message}))

