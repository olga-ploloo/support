from django.contrib import admin

from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    # fields = ['role']
    # pass
    list_display = ['id', 'author', 'status', 'updated_at']
