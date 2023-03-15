from rest_framework.viewsets import GenericViewSet

from .models import Message
from .serializers import MessageSerializer

from rest_framework import mixins


class MessageViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
