from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
    # list_display = ['email', 'role', 'username']
