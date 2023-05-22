from django.contrib.auth import get_user_model
from django.db import models


class Ticket(models.Model):
    class TicketStatus(models.TextChoices):
        SOLVED = 'SOLVED'
        UNSOLVED = 'UNSOLVED'
        FROZEN = 'FROZEN'

    title = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='tickets_from_customer'
    )
    status = models.CharField(
        max_length=8,
        choices=TicketStatus.choices,
        default=TicketStatus.UNSOLVED
    )
    description = models.TextField(blank=False)
    image = models.ImageField(upload_to='ticket', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.status} - {self.created_at.strftime("%Y-%m-%d%H:%M:%S")}'


class AssignTicket(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name='assigned_ticket')
    is_assign = models.BooleanField(default=False)
    assigned_support = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='tickets_by_support'
    )