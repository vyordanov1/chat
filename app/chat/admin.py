from django.contrib import admin
from .models import OffensiveWords, Message
#
#
# @admin.register(Admins)
# class AdminsAdmin(admin.ModelAdmin):
#     list_display = ('user', 'is_admin')


@admin.register(OffensiveWords)
class OffensiveWordsAdmin(admin.ModelAdmin):
    list_display = ('id', 'word')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'content')
