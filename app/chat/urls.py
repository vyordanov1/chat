from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin_page, name='admin'),
    path('manage_rooms/', manage_rooms, name='manage_rooms'),
    path('create_room/', create_room, name='create_room'),
    path('delete_room/<uuid:room_uuid>/', delete_room, name='delete_room'),
    path('members/', index, name='index'),
    path('login/', LoginView.as_view(
        template_name='chat/login.html'), name='login'),
    path('logout/', log_out, name='logout'),
    path('register/', register, name='register'),
    path('<str:room_name>/', room, name='room'),
    path('group/<str:group_uuid>/', group_chat, name='group_chat'),
    path('', index, name='none'),
]