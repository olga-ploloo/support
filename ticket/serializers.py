from rest_framework import serializers

from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    messages = serializers.StringRelatedField(many=True, read_only=True)
    author = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = '__all__'
        extra_kwargs = {
            'description': {
                'required': True,
            },
        }


class AssignTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'is_assign', 'assigned_support']
