from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from backend.message.models import Message


@receiver(post_save, sender=Message)
def notification_message_post_save(sender, instance, created, **kwargs):
    print('notification_message_post_save')
    if not created:
        return
    # писать в базу notice?
    channel_layer = get_channel_layer()
    print(channel_layer)
    async_to_sync(channel_layer.group_send)(
        'notifications',
        {
            'type': 'notify',
            'message': 'New model created!'
        }
    )