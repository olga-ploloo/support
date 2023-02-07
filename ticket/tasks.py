from django.conf import settings

from celery import shared_task
from django.core.mail import send_mail
from .models import Ticket


@shared_task
def send_email(ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    subject = 'Support System: Your ticket status has been changed'
    message = f'The status of your ticket has been changed to {ticket.status}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [ticket.author, ]
    send_mail(
        subject,
        message,
        email_from,
        recipient_list,
        fail_silently=False,
    )
