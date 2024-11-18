from django.urls import re_path
from chat.consumers import *


### URL routing for websocket consumers ###
websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/members/$", MembersConsumer.as_asgi()),
    re_path(r"ws/index/$", IndexCounterConsumer.as_asgi())
]