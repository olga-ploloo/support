from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    # fields = ['role']
    pass
    # list_display = ['email', 'role', 'username']