import json
import time
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from django.template.loader import render_to_string
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .views import get_active_users


class IndexCounterConsumer(AsyncWebsocketConsumer):
    RUNNING_TASK = True

    async def connect(self):
        self.RUNNING_TASK = True
        await self.accept()
        await asyncio.create_task(self.send_data())

    async def disconnect(self, exit_code):
        self.RUNNING_TASK = False
        await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def send_data(self):
        while self.RUNNING_TASK:
            active_users = await self.get_active_users()
            public_rooms = await self.get_public_rooms()
            messages_sent = await self.get_messages_sent()
            payload = {
                "active_users": {
                    "count": active_users,
                    "title": "Users Trusting Us"
                },
                "public_rooms": {
                    "count": public_rooms,
                    "title": "Public Rooms"
                },
                "messages_sent": {
                    "count": messages_sent,
                    "title": "Messages Sent"
                },
                "site_visits": {
                    "count": 0,
                    "title": "Site Visits"
                }
            }
            await self.send(text_data=json.dumps(payload))
            await asyncio.sleep(5)


    @database_sync_to_async
    def get_active_users(self):
        return len([u.pk for u in User.objects.filter(is_active=True)])

    @database_sync_to_async
    def get_public_rooms(self):
        from .models import ChatRoom
        return len([r for r in ChatRoom.objects.filter(is_public=True)])

    @database_sync_to_async
    def get_messages_sent(self):
        from .models import Message
        return len([m for m in Message.objects.all()])



class MembersConsumer(AsyncWebsocketConsumer):
    RUNNING_TASK = True

    async def connect(self):
        self.RUNNING_TASK = True
        await self.accept()
        await asyncio.create_task(self.send_users())

    async def disconnect(self, close_code):
        self.RUNNING_TASK = False
        await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def send_users(self, logged_in_users=None):
        while self.RUNNING_TASK:
            if not self.scope['user'].is_authenticated:
                self.RUNNING_TASK = False
                await self.close()
                return

            logged_in_users = await self.get_active_users()
            await self.send(text_data=json.dumps(
                logged_in_users
            ))
            await asyncio.sleep(5)

    @database_sync_to_async
    def get_active_users(self):
        from django.contrib.sessions.models import Session
        from django.utils import timezone
        logged_user = self.scope['user']
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        user_ids = []
        for session in sessions:
            data = session.get_decoded()
            user_id = data.get('_auth_user_id', None)
            if user_id:
                user_ids.append(user_id)

        return {
            'all_users': {
                user.pk: user.username for user in User.objects.filter(is_active=True)
            },
            'logged_user': {
                logged_user.id: logged_user.username
            },
            'logged_users': {
                user.id: user.username for user in User.objects.filter(id__in=user_ids)
            }
        }


class ChatConsumer(WebsocketConsumer):
    """
    Consumer class to handle message exchange in the chat app
    """
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        #Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        #Leave room
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    #Receive message from Websocket
    def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        time = text_data_json['time']
        username = text_data_json['username']

        #send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat.message",
                "message": message,
                "time": time,
                "username": username
            }
        )

    #Receive message from room group
    def chat_message(self, event):
        message = event['message']
        time = event['time']
        username = event['username']

        #send message to websocket
        self.send(text_data=json.dumps({
            "message": message,
            "time": time,
            "username": username
        }
        ))


















