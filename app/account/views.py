import json
import uuid, logging

from django.contrib.auth.models import User
from django.contrib.messages.storage.cookie import MessageSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
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
from django.contrib.auth.decorators import user_passes_test

# Create your views here.


def is_admin(user):
    return user.admins.is_admin


@user_passes_test(is_admin)
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


@user_passes_test(is_admin)
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


@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = User.objects.get(pk=user_id)
    form = EditUserForm(request.POST or None,
                        instance=Admins.objects.get_or_create(
                            user_id=user_id,
                        )[0])

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('manage_users')

    payload = {
        "page_data": {
            "header": "Edit User",
            "leave_btn": {
                "url": "manage_users",
                "name": "Return"
            }
        },
        "form": form,
        "u": user,
    }
    return render(request, 'account/admin/edit_user.html', payload)


@user_passes_test(is_admin)
def delete_user(request, user_id):
    if request.method == "GET":
        user = get_object_or_404(User, id=user_id)
        user.delete()
    return redirect("manage_users")

@user_passes_test(is_admin)
def create_room(request):
    if request.method == "GET":
        ChatRoom.objects.create(
            is_public=True
        )
        return redirect("manage_rooms")

@user_passes_test(is_admin)
def delete_room(request, room_uuid):
    if request.method == "GET":
        room = get_object_or_404(ChatRoom, uuid=room_uuid)
        room.delete()
    return redirect('manage_rooms')


def account(request):
    profile_form = ProfileForm(request.POST, instance=request.user)
    if request.method == "POST":
        if profile_form.is_valid():
            profile_form.save()

    payload = {
        "page_data": {
            "header": "Account Page",
            "leave_btn": {
                "url": "index",
                "name": "Return"
            }
        },
        "user": request.user,
        "form": profile_form,
    }
    return render(request, 'account/profile.html', context=payload)


def upload_image(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES,
                         instance=request.user.profile or None)
        if form.is_valid():
            form.save()
            return redirect('account')


def select_theme(request):
    themes = Themes.objects.all()
    if request.method == 'POST':
        theme_id = request.POST.get('theme')
        theme = Themes.objects.get(id=theme_id)
        user = request.user
        user.profile.theme_preference = theme
        user.profile.save()
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


@user_passes_test(is_admin)
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


@user_passes_test(is_admin)
def delete_theme(request, theme_id):
    if request.method == "GET":
        theme = get_object_or_404(Themes, pk=theme_id)
        theme.delete()
    return redirect('manage_themes')
