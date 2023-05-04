from django.contrib.auth import get_user_model
from django.db import models


class Notification(models.Model):
    user_sender = models.ForeignKey(get_user_model(), null=True, blank=True, related_name='user_sender',
                                    on_delete=models.CASCADE)
    user_receiver = models.ForeignKey(get_user_model(), null=True, blank=True, related_name='user_receiver',
                                      on_delete=models.CASCADE)
    status = models.CharField(max_length=100, null=True, blank=True, default="unread")
    type_of_notification = models.CharField(max_length=100, null=True, blank=True)
