from django.urls import re_path
from chat.consumers import *

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/members/$", MembersConsumer.as_asgi()),
    re_path(r"ws/index/$", IndexCounterConsumer.as_asgi())
]