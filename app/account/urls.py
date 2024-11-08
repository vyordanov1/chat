from django.urls import path, include
from .views import *
from login.views import UserPasswordChange

urlpatterns = [
    path('themes/', select_theme, name='select_theme'),
    path('manage_rooms/', ManageRoomsView.as_view(), name='manage_rooms'),
    path('manage_themes/', ManageThemesView.as_view(), name='manage_themes'),
    path('manage_users/', ManageUsersView.as_view(), name='manage_users'),
    path('create_room/', CreateRoomView.as_view(), name='create_room'),
    path('delete_room/<uuid:room_uuid>/', DeleteRoomView.as_view(), name='delete_room'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),
    path('delete_theme/<int:theme_id>/', DeleteThemesView.as_view(), name='delete_theme'),
    path('user-password-change/<int:user_id>/', UserPasswordChange.as_view(), name='user_password_change'),
    path('upload/', UploadImageView.as_view(), name='upload_image'),
    path('', AccountView.as_view(), name='account'),
]
