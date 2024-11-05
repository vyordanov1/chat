from django.urls import path, include
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('members/', MembersView.as_view(), name='index'),
    path('<str:room_name>/', ChatRoomView.as_view(), name='room'),
    path('group/<str:group_uuid>/', GroupChatView.as_view(), name='group_chat'),
    path('api/send-message/', send_message, name='send_message'),
    path('', MembersView.as_view(), name='none'),
]
