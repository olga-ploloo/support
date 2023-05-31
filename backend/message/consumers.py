import json

from channels.db import database_sync_to_async
from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer

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
        user = (self.scope['user'])
        self.group_name = f'chat_{self.room_name}'
        # print(user)
        # print('!!!!!!!!!!!!')
        # self.room_group_name = str(ticket_id)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name,
        # )
        # await self.send(text_data='hello? we connected!')
        self.channel_layer.group_send(
            self.group_name,
            {
                'message': 'hello? we connected!',
            }
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print("WebSocket Chat Disconnected!")
        #     await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        #     await self.disconnect(code)

    async def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope['user']
        ticket_id = self.scope['url_route']['kwargs']['ticket_id']

        await self.save_message(user, message, ticket_id)
        self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_message',
                'message': message,
            }
        )
        # await self.send(text_data=json.dumps({"message": message}))

    async def send_message(self, event):
        print('send message')
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
    # @database_sync_to_async
    # def get_messages(self):
    #     custom_serializers = MessageSerializer()
    #     messages = custom_serializers.serialize(
    #         Message.objects.select_related().filter(thread_name=self.room_group_name),
    #         fields=(
    #             'sender__pk',
    #             'sender__username',
    #             'sender__last_name',
    #             'sender__first_name',
    #             'sender__email',
    #             'sender__last_login',
    #             'sender__is_staff',
    #             'sender__is_active',
    #             'sender__date_joined',
    #             'sender__is_superuser',
    #             'message',
    #             'thread_name',
    #             'timestamp',
    #         ),
    #     )
    #     return messages

    @database_sync_to_async
    def save_message(self, author, message, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        Message.objects.create(author=author, message=message, ticket=ticket)
