from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('members/', index, name='index'),
    path('login/', LoginView.as_view(
        template_name='chat/login.html'), name='login'),
    path('logout/', log_out, name='logout'),
    path('register/', register, name='register'),
    path('<str:room_name>/', room, name='room'),
    path('', index, name='none'),
]