from django.urls import re_path
from chat.consumers import *


### URL routing for websocket consumers ###
websocket_urlpatterns = [
    re_path(r"wss/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"wss/members/$", MembersConsumer.as_asgi()),
    re_path(r"wss/index/$", IndexCounterConsumer.as_asgi())
]
