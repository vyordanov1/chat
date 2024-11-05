from django.urls import path, include
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', LoginView.as_view(
        template_name='login/login.html'), name='login'),
    path('logout/', log_out, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-change/<uuid:uuid>/', PasswordChangeView.as_view(), name='password_change'),
]
