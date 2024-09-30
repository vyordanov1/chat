from django.contrib import admin
from .models import Admins

# Register your models here.

@admin.register(Admins)
class AdminsAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_admin')
