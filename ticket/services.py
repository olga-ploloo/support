from django.conf import settings
from .tasks import send_email

from .models import Ticket


def status_update_notification(ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    subject = 'Support System: Your ticket status has been changed'
    message = f'The status of your ticket has been changed to {ticket.status}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [ticket.author, ]
    send_email.delay(
        subject,
        message,
        email_from,
        recipient_list,
    )
