from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Ticket(models.Model):
    class TicketStatus(models.TextChoices):
        SOLVED = 'SOLVED'
        UNSOLVED = 'UNSOLVED'
        FROZEN = 'FROZEN'

    title = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tickets'
    )
    status = models.CharField(
        max_length=8,
        choices=TicketStatus.choices,
        default=TicketStatus.UNSOLVED
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # created_at = models.DateTimeField('created at', auto_now_add=True)
    # updated_at = models.DateTimeField('updated at', auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.status} - {self.created_at.strftime("%Y-%m-%d%H:%M:%S")}'
