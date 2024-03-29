from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(subject,
               message,
               email_from,
               recipient_list):
    send_mail(
        subject,
        message,
        email_from,
        recipient_list,
        fail_silently=False,
    )
