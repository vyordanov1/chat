from django.contrib import admin
from .models import OffensiveWords, Message
from unfold.admin import ModelAdmin

#
#
# @admin.register(Admins)
# class AdminsAdmin(admin.ModelAdmin):
#     list_display = ('user', 'is_admin')


@admin.register(OffensiveWords)
class OffensiveWordsAdmin(ModelAdmin):
    list_display = ('id', 'word')


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ('id', 'sender', 'content')
