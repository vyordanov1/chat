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
from .models import *
from account.models import Profile


logger = logging.getLogger(__name__)


# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    logged_in_users = get_active_users()
    rooms = ChatRoom.objects.all()
    payload = {
        "users": User.objects.all().exclude(
            username=request.user.username,
        ),
        "logged_in_users": logged_in_users,
        "page_data": {
            "leave_btn": {
                "url": "logout",
                "name": "Logout"
            },
            "header": "Chat members",
        },
        "rooms": rooms
    }
    return render(request, 'chat/members.html', context=payload)


def room(request, room_name):
    chat_user = User.objects.get(
        id=Profile.objects.get(
            uuid=room_name
        ).user_id
    )
    chat_room = get_or_create_room(request.user, chat_user)
    messages = get_message_history(chat_room)

    payload = {
        "page_data": {
            "leave_btn": {
                "url": "index",
                "name": "Leave Chat"
            },
        },
        "chat_user": chat_user,
        "room_name": chat_room.uuid_redacted,
        "room": {
            "name": chat_user.username
        },
        "chat_messages": messages,
    }
    # return JsonResponse(context)
    return render(request, template_name='chat/room.html', context=payload)


def get_message_history(room):
    chat_messages = Message.objects.filter(
        chat_room_id=room.id
    ).order_by('timestamp')

    messages = {}
    for m in chat_messages:
        if m.id not in messages:
            messages.update({
                m.id: {
                    'username': get_object_or_404(User, id=m.sender_id).username,
                    'message': m.content,
                    'time': m.timestamp.strftime('%d.%m.%Y %H:%M:%S')
                }
            })
    return messages


def group_chat(request, group_uuid):
    room = ChatRoom.objects.get(uuid=group_uuid)
    messages = get_message_history(room)

    payload = {
        "page_data": {
            "leave_btn": {
                "url": "index",
                "name": "Leave Chat"
            },
            "chat_user": None,
        },
        "room": room,
        "chat_messages": messages,
        "room_name": room.uuid_redacted
    }
    return render(request, 'chat/room.html', context=payload)


def get_or_create_room(user, dest_user):
    if user.id > dest_user.id:
        user, dest_user = dest_user, user

    chat_room = ChatRoom.objects.filter(
        userchatroom__user=user
    ).filter(
        userchatroom__user=dest_user
    ).first()

    if not chat_room:
        chat_room = ChatRoom.objects.create()
        chat_room.uuid_redacted = str(chat_room.uuid).replace('-', '')
        chat_room.name = '-'.join([user.username, dest_user.username])
        chat_room.save()
        UserChatRoom.objects.create(user=user, chat_room=chat_room)
        UserChatRoom.objects.create(user=dest_user, chat_room=chat_room)

    return chat_room


def get_active_users():
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_ids = []
    for session in sessions:
        data = session.get_decoded()
        user_id = data.get('_auth_user_id', None)
        if user_id:
            user_ids.append(user_id)

    logged_in_users = [u.id for u in User.objects.filter(id__in=user_ids)]

    return logged_in_users


def send_message(request):
    """
    Endpoint to save a message to the db for later use
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data.get('content')
        sender = data.get('sender')
        room = data.get('room')

        room_obj = get_object_or_404(ChatRoom, uuid_redacted=room)
        sender_obj = get_object_or_404(User, username=sender)

        message = Message.objects.create(
            sender=sender_obj,
            content=content,
            chat_room=room_obj
        )

        return JsonResponse({
            'status': 'Message sent!',
            'message': message.id
        })
    return JsonResponse({
        'error': 'Invalid request'}, status=400
    )

