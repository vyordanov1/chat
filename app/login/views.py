import json
import uuid, logging
from django.contrib.auth.models import User
from django.contrib.messages.storage.cookie import MessageSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.sessions.models import Session
from django.utils import timezone
from random_word import RandomWords
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib import messages
from .forms import *


# Create your views here.

logger = logging.getLogger(__name__)

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,
                            username=username,
                            password=password)
        if user is not None:
            login(request, user)

            next_page = request.POST.get('next') or request.GET.get('next')
            if next_page:
                return HttpResponseRedirect(next_page)
            return redirect('index')
        else:
            messages.info(request, 'Failed authentication!')
    payload = {}
    return render(request, 'login/login.html', payload)


def log_out(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully registered")
            return redirect('index')
    else:
        form = RegistrationForm()
    payload = {'form': form}
    return render(request, 'login/register.html', context=payload)


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST or None)
        if form.is_valid():
            reset_request = generate_password_reset_request(
                user_id=form.cleaned_data['user_id']
            )
            return redirect('password_change', uuid=reset_request.uuid)
    else:
        form = PasswordResetForm()
    payload = {'form': form}
    return render(request, 'login/password_reset.html', context=payload)


def password_change(request, uuid):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST or None)
        if form.is_valid():
            user = request.user
            password = form.cleaned_data['password1']
            reset_request = get_object_or_404(PasswordReset, uuid=uuid)
            if not reset_request.is_active:
                form.add_error('password1', 'This URL is no longer active!')
                return render(request, 'login/password_change.html', {'form': form})
            user.set_password(password)
            user.save()
            reset_request.done()
            return redirect('index')
    else:
        reset_request = PasswordReset.objects.get(uuid=uuid)
        if reset_request.is_done:
            return redirect('index')
        form = PasswordChangeForm()
    payload = {'form': form}
    return render(request, 'login/password_change.html', context=payload)


def user_password_change(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST or None)
        if form.is_valid():
            password = form.cleaned_data['password1']
            reset_request = PasswordReset.objects.filter(
                user_id=user.id,
            ).last()
            user.set_password(password)
            user.save()
            reset_request.done()
            user = authenticate(
                username=user.username,
                password=password
            )
            login(request, user)
            return redirect('account')

    generate_password_reset_request(user_id)
    form = PasswordChangeForm()
    payload = {
        "page_data": {
            "header": "Account Page",
            "leave_btn": {
                "url": "index",
                "name": "Return"
            }
        },
        "user": request.user,
        "form": form
    }
    return render(request,'account/password_change.html', context=payload)


def generate_password_reset_request(user_id):
    user = get_object_or_404(User, id=user_id)
    if user is not None:
        reset_request = PasswordReset.objects.create(
            user=user,
            uuid=uuid.uuid4(),
        )
        reset_request.save()
        return reset_request