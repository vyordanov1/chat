from django.urls import path, include
from .views import *
from login.views import user_password_change

urlpatterns = [
    path('themes/', select_theme, name='select_theme'),
    path('manage_rooms/', manage_rooms, name='manage_rooms'),
    path('manage_themes/', manage_themes, name='manage_themes'),
    path('manage_users/', manage_users, name='manage_users'),
    path('create_room/', create_room, name='create_room'),
    path('delete_room/<uuid:room_uuid>/', delete_room, name='delete_room'),
    path('edit_user/<int:user_id>', edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('delete_theme/<int:theme_id>/', delete_theme, name='delete_theme'),
    path('user-password-change/<int:user_id>/', user_password_change, name='user_password_change'),
    path('upload/', upload_image, name='upload_image'),
    path('', account, name='account'),
]
