from django.contrib import admin
from .models import OffensiveWords, Message
from unfold.admin import ModelAdmin


@admin.register(OffensiveWords)
class OffensiveWordsAdmin(ModelAdmin):
    list_display = ('id', 'word')


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ('id', 'sender', 'content')
