from rest_framework import serializers

from .models import AssignTicket, Ticket


class AssignTicketSerializer(serializers.ModelSerializer):
    assigned_support = serializers.StringRelatedField(many=False)

    class Meta:
        model = AssignTicket
        fields = ['is_assign', 'assigned_support']


class TicketSerializer(serializers.ModelSerializer):
    messages = serializers.StringRelatedField(many=True, read_only=True)
    author = serializers.StringRelatedField()
    assigned_ticket = AssignTicketSerializer()

    class Meta:
        model = Ticket
        fields = '__all__'
        extra_kwargs = {
            'description': {
                'required': True,
            },
        }


class TicketCreateSerializer(serializers.ModelSerializer):
    author = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        exclude = ['status']
        extra_kwargs = {
            'description': {
                'required': True,
            },
        }
