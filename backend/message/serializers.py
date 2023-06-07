from rest_framework import serializers

from backend.ticket.models import Ticket

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all(), many=False)
    author = serializers.CharField(default=serializers.CurrentUserDefault())
    author_id = serializers.IntegerField(source='author.id')

    class Meta:
        model = Message
        fields = '__all__'
        extra_kwargs = {
            'message': {
                'required': True,
            },
        }


class MessageListSerializer(MessageSerializer):
    author_id = serializers.IntegerField(source='author.id')

    class Meta:
        model = Message
        fields = '__all__'
