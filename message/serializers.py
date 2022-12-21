from rest_framework import serializers

from ticket.models import Ticket
from user.models import User
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all(),
                                                  many=False)

    class Meta:
        model = Message
        fields = ('ticket', 'author', 'message', 'created_at', 'ticket')



