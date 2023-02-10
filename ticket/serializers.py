from rest_framework import serializers

from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    messages = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Ticket
        # fields = ('author', 'status', 'description', 'messages')
        fields = '__all__'
        extra_kwargs = {
            'description': {
                'required': True,
            },
        }
