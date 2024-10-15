import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


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


















