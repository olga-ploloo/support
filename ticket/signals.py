from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from ticket.models import AssignTicket, Ticket


@receiver(post_save, sender=Ticket)
def create_assign_ticket(sender, instance, created, **kwargs):
    if created:
        AssignTicket.objects.create(
            ticket=instance,
        )


@receiver(post_save, sender=Ticket)
def send_ticket_notification(sender, instance, **kwargs):
    notification = 'New ticket has been created'
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        str(instance.id),
        {
            'type': 'send_notification',
            'notification': notification
        }
    )
