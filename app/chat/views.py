import json
import uuid, logging

from django.contrib.auth.models import User
from django.contrib.messages.storage.cookie import MessageSerializer
from django.shortcuts import render, redirect, get_object_or_404
from chat.forms import *
from django.contrib.auth import login, authenticate, logout
from chat.forms import RegistrationForm
from django.http import HttpResponseRedirect, JsonResponse
from .forms import ProfileForm, ThemeForm, SearchForm
from .models import Profile, ChatRoom, UserChatRoom, Message, Themes, PasswordReset
from django.contrib.sessions.models import Session
from django.utils import timezone
from random_word import RandomWords
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib import messages


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
    return render(request, 'chat/register.html', context=payload)


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
    return render(request, 'chat/password_reset.html', context=payload)


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

    reset_request = generate_password_reset_request(user_id)
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
    return render(request,'chat/account/password_change.html', context=payload)


def generate_password_reset_request(user_id):
    user = get_object_or_404(User, id=user_id)
    if user is not None:
        reset_request = PasswordReset.objects.create(
            user=user,
            uuid=uuid.uuid4(),
        )
        reset_request.save()
        return reset_request


def password_change(request, uuid):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST or None)
        if form.is_valid():
            password = form.cleaned_data['password1']
            reset_request = PasswordReset.objects.get(uuid=uuid)
            user = reset_request.user
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
    return render(request, 'chat/password_change.html', context=payload)


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
    return render(request, 'chat/login.html', payload)


def log_out(request):
    logout(request)
    return redirect('login')

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
            "chat_user": chat_user,
            "room_name": chat_room.uuid_redacted,
        },
        "room": {"name": chat_user.username},
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
            "room_name": room.uuid_redacted
        },
        "room": room,
        "chat_messages": messages,
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
    return render(request, 'chat/admin/manage_rooms.html', context=payload)


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
    return render(request, "chat/admin/manage_users.html", context=payload)


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


def send_message(request):
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
    return render(request, 'chat/account/profile.html', context=payload)


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
    return render(request, 'chat/account/themes.html', context=payload)



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
    return render(request, 'chat/admin/themes.html', context=payload)


def delete_theme(request, theme_id):
    if request.method == "GET":
        theme = get_object_or_404(Themes, pk=theme_id)
        theme.delete()
    return redirect('manage_themes')


# def change_theme(request, theme_id):
#     user = request.user
#     if request.method == "GET":
#         theme = get_object_or_404(Themes, pk=theme_id)
#         user.theme_preference = theme
#         user.save()
#         return redirect('select_theme')




