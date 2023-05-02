from rest_framework import serializers

from .models import AssignTicket, Ticket


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
    ticket = serializers.StringRelatedField(many=False)
    assigned_support = serializers.StringRelatedField(many=False)

    class Meta:
        model = AssignTicket
        fields = ['id', 'ticket', 'is_assign', 'assigned_support']
