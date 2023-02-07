from celery import shared_task
from django.core.mail import send_mail
from .models import Ticket


@shared_task
def send_email(ticket_id):
    # ticket = Ticket.objects.get(id=ticket_id)
    send_mail(
        'Subject here',
        'Here is the message.',
        'from@example.com',
        ['eli4ka@tut.by'],
        # fail_silently=False,
    )
