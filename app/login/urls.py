from django.urls import path, include
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', LoginView.as_view(
        template_name='login/login.html'), name='login'),
    path('logout/', log_out, name='logout'),
    path('register/', register, name='register'),
    path('password-reset/', password_reset, name='password_reset'),
    path('password-change/<uuid:uuid>/', password_change, name='password_change'),
    path('user-password-change/<int:user_id>/', user_password_change, name='user_password_change'),

]
