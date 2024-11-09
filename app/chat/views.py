import json, logging
import time
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView
from .models import *
from account.models import Profile
from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from app.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


# Create your views here.
def is_user_blocked(user):
    time_now = int(time.time())
    blocked_until = user.profile.blocked_until

    if blocked_until is not None:
        return time_now > int(blocked_until.timestamp())
    return True


class MembersView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/members.html'
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        time_now = int(time.time())
        user = request.user
        if user.profile.blocked and user.profile.blocked_until is not None:
            if time_now > int(user.profile.blocked_until.timestamp()):
                user.profile.blocked_until = None
                user.profile.blocked = False
                user.profile.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        payload = super().get_context_data(**kwargs)
        rooms = ChatRoom.objects.all()
        payload.update({
            "users": User.objects.all().exclude(
                username=self.request.user.username
            ),
            # "logged_in_users": logged_in_users['logged_users'].keys(),
            "page_data": {
                "header": "Chat members",
            },
            "rooms": rooms
        })
        return payload


@method_decorator(user_passes_test(is_user_blocked), name='dispatch')
class ChatRoomView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/room.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        payload = super().get_context_data(**kwargs)
        room_name = self.kwargs['room_name']
        chat_user = User.objects.get(
            id=Profile.objects.get(
                uuid=room_name
            ).user_id
        )
        chat_room = get_or_create_room(self.request.user, chat_user)
        messages = get_message_history(chat_room)
        payload.update({
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
        })
        return payload


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


@method_decorator(user_passes_test(is_user_blocked), name='dispatch')
class GroupChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/room.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        payload = super().get_context_data(**kwargs)
        group_uuid = self.kwargs.get('group_uuid')
        room = ChatRoom.objects.get(uuid=group_uuid)
        messages = get_message_history(room)
        payload.update({
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
        })
        return payload


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

def get_active_users(logged_user=None):
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_ids = []
    for session in sessions:
        data = session.get_decoded()
        user_id = data.get('_auth_user_id', None)
        if user_id:
            user_ids.append(user_id)

    return {
        'logged_user': {
            logged_user.id: logged_user.username
        },
        'logged_users': {
            user.id: user.username for user in User.objects.filter(id__in=user_ids)
        }
    }


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


class SendMessageView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        pass



