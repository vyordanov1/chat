import json
import uuid, logging
from django.contrib.auth.models import User
from django.contrib.messages.storage.cookie import MessageSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.sessions.models import Session
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, FormView
from random_word import RandomWords
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib import messages
from .forms import *
from app.mixins import PageDataMixin


# Create your views here.

logger = logging.getLogger(__name__)

def log_out(request):
    logout(request)
    return redirect('login')


class RegisterView(CreateView):
    model = User
    template_name = 'login/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('index')


class PasswordResetView(FormView):
    template_name = 'login/password_reset.html'
    form_class = PasswordResetForm

    def form_valid(self, form):
        reset_request = generate_password_reset_request(
            user_id=form.cleaned_data['user_id'],
        )
        self.reset_request_uuid = reset_request.uuid
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('password_change', kwargs={'uuid': self.reset_request_uuid})


class PasswordChangeView(FormView):
    template_name = 'login/password_change.html'
    success_url = reverse_lazy('index')
    form_class = PasswordChangeForm
    slug_url_kwarg = 'uuid'
    slug_field = 'uuid'

    def form_valid(self, form):
        password = form.cleaned_data['password1']
        reset_request = get_object_or_404(PasswordReset, uuid=self.kwargs['uuid'])
        user = User.objects.get(pk=reset_request.user.id)
        if not reset_request.is_active:
            self.form.add_error('password1', 'This URL is no longer active!')
            return self.form_invalid(form)
        user.set_password(password)
        user.save()
        reset_request.done()
        return super().form_valid(form)


class UserPasswordChange(FormView):
    template_name = 'account/password_change.html'
    success_url = reverse_lazy('account')
    pk_url_kwarg = 'user_id'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        user = self.request.user
        password = form.cleaned_data['password1']
        reset_request = PasswordReset.objects.filter(
            user_id=self.kwargs['user_id'],
        ).last()
        user.set_password(password)
        user.save()
        reset_request.done()
        user = authenticate(
            username=user.username,
            password=password
        )
        login(self.request, user)
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        generate_password_reset_request(self.kwargs['user_id'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        payload = super().get_context_data(**kwargs)
        payload['page_data'] = {
            "header": "Account Page",
            "leave_btn": {
                "url": "index",
                "name": "Return"
            }
        }
        return payload


def generate_password_reset_request(user_id):
    user = get_object_or_404(User, id=user_id)
    if user is not None:
        reset_request = PasswordReset.objects.create(
            user=user,
            uuid=uuid.uuid4(),
        )
        reset_request.save()
        return reset_request