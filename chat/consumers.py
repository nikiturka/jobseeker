from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'chat_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        user_email = data['user']
        room = data['room']

        await self.save_message(user_email, room, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user_email,
                'room': room
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user_email = event['user']
        room = event['room']

        await self.send(text_data=json.dumps({
            'message': message,
            'user': user_email,
            'room': room
        }))

    @sync_to_async
    def save_message(self, user_email, room, content):
        from main.models import CustomUser
        from .models import Message, Room

        user = CustomUser.objects.get(email=user_email)
        room = Room.objects.get(pk=room)

        Message.objects.create(
            user=user,
            room=room,
            content=content
        )
