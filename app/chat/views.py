import logging
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from chat.forms import *
from django.contrib.auth import login, authenticate, logout
from chat.forms import RegistrationForm
from django.http import HttpResponseRedirect
from django.db.models.functions import Replace
from django.db.models import F
from .models import Profile

logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    payload = {
        'users': User.objects.all().exclude(
            username=request.user.username,
        ),
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
    logger.info('User logged out')
    logout(request)
    return redirect('login')


def room(request, room_name):
    chat_user = User.objects.get(
        id=Profile.objects.get(
            uuid=room_name
        ).user_id
    )

    context = {
        "room_name": room_name,
        "chat_user": chat_user
    }
    return render(request, template_name='chat/room.html', context=context)






