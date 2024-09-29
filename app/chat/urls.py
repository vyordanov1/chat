from django.urls import path, include
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('account/', account, name='account'),
    path('themes/', select_theme, name='select_theme'),
    path('manage_rooms/', manage_rooms, name='manage_rooms'),
    path('manage_themes/', manage_themes, name='manage_themes'),
    path('manage_users/', manage_users, name='manage_users'),
    path('create_room/', create_room, name='create_room'),
    path('delete_room/<uuid:room_uuid>/', delete_room, name='delete_room'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('delete_theme/<int:theme_id>/', delete_theme, name='delete_theme'),
    path('members/', index, name='index'),
    path('login/', LoginView.as_view(
        template_name='chat/login.html'), name='login'),
    path('logout/', log_out, name='logout'),
    path('register/', register, name='register'),
    path('password-reset/', password_reset, name='password_reset'),
    path('password-change/<uuid:uuid>/', password_change, name='password_change'),
    path('user-password-change/<int:user_id>/', user_password_change, name='user_password_change'),
    path('<str:room_name>/', room, name='room'),
    path('group/<str:group_uuid>/', group_chat, name='group_chat'),
    path('api/send-message/', send_message, name='send_message'),
    path('', index, name='none'),
]
