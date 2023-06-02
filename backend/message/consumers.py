import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from backend.message.models import Message
from backend.message.serializers import MessageSerializer
from backend.ticket.models import Ticket


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.group_name = None

    async def connect(self):
        print("WebSocket Chat Connected!")
        self.room_name = self.scope['url_route']['kwargs']['ticket_id']
        self.group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print("WebSocket Chat Disconnected!")
        await self.disconnect(code)

    async def receive(self, text_data=None, bytes_data=None):
        """Receive message from client, save message and send to chat serialized new message. """
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope['user']
        ticket_id = self.scope['url_route']['kwargs']['ticket_id']
        new_message = await self.save_message(user, message, ticket_id)
        serialized_message = MessageSerializer(new_message).data

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_message',
                'message': serialized_message,
            }
        )

    async def send_message(self, event):
        message = event["message"]
        text_data = json.dumps({"message": message})
        await self.send(text_data)

    @database_sync_to_async
    def save_message(self, author, message, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        return Message.objects.create(author=author,
                                      message=message,
                                      ticket=ticket)
