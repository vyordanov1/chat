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
from .models import *
from login.views import generate_password_reset_request
from chat.models import ChatRoom, UserChatRoom

# Create your views here.


def manage_rooms(request):
    chat_rooms = ChatRoom.objects.all()
    form = SearchForm(request.POST or None)
    rooms = []
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            chat_rooms = chat_rooms.filter(name__icontains=query)

    for r in chat_rooms:
        if r.uuid not in rooms:
            rooms.append(
                {
                    "id": r.id,
                    "uuid": r.uuid,
                    "name": r.name,
                    "members": [u.user for u in UserChatRoom.objects.filter(
                        chat_room_id=r.id
                    )]
                }
            )

    payload = {
        "page_data": {
            "header": "Existing Chat Rooms",
            "leave_btn": {
                "url": "account",
                "name": "Return"
            }
        },
        "rooms": rooms,
        "form": form,
    }
    return render(request, 'account/admin/manage_rooms.html', context=payload)


def manage_users(request):
    users = User.objects.all()
    form = SearchForm(request.POST or None)

    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            users = users.filter(username__icontains=query)

    payload = {
        "page_data": {
            "header": "Existing Chat Users",
            "leave_btn": {
                "url": "account",
                "name": "Return"
            }
        },
        "users": users,
        "form": form,
    }
    return render(request, "account/admin/manage_users.html", context=payload)


def delete_user(request, user_id):
    if request.method == "GET":
        user = get_object_or_404(User, id=user_id)
        user.delete()
    return redirect("manage_users")


def create_room(request):
    r = RandomWords()
    room = ChatRoom.objects.create()
    room.uuid_redacted = str(room.uuid).replace('-', '')
    room.is_public = True
    room.name = r.get_random_word()
    room.save()

    return redirect('manage_rooms')


def delete_room(request, room_uuid):
    if request.method == "GET":
        room = get_object_or_404(ChatRoom, uuid=room_uuid)
        room.delete()
    return redirect('manage_rooms')


def account(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('account')

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
    return render(request, 'account/profile.html', context=payload)


def select_theme(request):
    themes = Themes.objects.all()
    if request.method == 'POST':
        theme_id = request.POST.get('theme')
        theme = Themes.objects.get(id=theme_id)
        user = request.user
        user.profile.theme_preference = theme
        user.save()
        return redirect('select_theme')

    payload = {
        "page_data": {
            "header": "Themes",
            "leave_btn": {
                "url": "index",
                "name": "Return"
            }
        },
        "user": request.user,
        "themes": themes,
    }
    return render(request, 'account/themes.html', context=payload)


def manage_themes(request):
    form = ThemeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('manage_themes')
    themes = Themes.objects.all()
    payload = {
        "page_data": {
            "header": "Themes",
            "leave_btn": {
                "url": "account",
                "name": "Return"
            },
        },
        "user": request.user,
        "themes": themes,
        "form": form
    }
    return render(request, 'account/admin/themes.html', context=payload)


def delete_theme(request, theme_id):
    if request.method == "GET":
        theme = get_object_or_404(Themes, pk=theme_id)
        theme.delete()
    return redirect('manage_themes')

