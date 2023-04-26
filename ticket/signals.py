from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from ticket.models import AssignTicket, Ticket

User = get_user_model


@receiver(post_save, sender=Ticket)
def create_assign_ticket(sender, instance, created, **kwargs):
    if created:
        AssignTicket.objects.create(
            ticket=instance,
            )
