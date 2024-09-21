from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from chat.forms import *
from django.contrib.auth import login, authenticate, logout
from chat.forms import RegistrationForm
from django.http import HttpResponseRedirect
from .models import Profile, ChatRoom, UserChatRoom
from django.contrib.sessions.models import Session
from django.utils import timezone

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    logged_in_users = get_active_users()
    payload = {
        'users': User.objects.all().exclude(
            username=request.user.username,
        ),
        'logged_in_users': logged_in_users,
    }
    return render(request, 'chat/index.html', context=payload)

def register(request):
    form = RegistrationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('index')
    else:
        form = RegistrationForm()
    payload = {'form': form}
    return render(request, 'chat/register.html', context=payload)


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
    logged_in_users = get_active_users()

    context = {
        "room_name": chat_room.uuid_redacted,
        "chat_user": chat_user,
    }
    # return JsonResponse(context)
    return render(request, template_name='chat/room.html', context=context)


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



