from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Message
from .serializers import MessageSerializer
from .services import customer_created_message_notification


class MessageViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_permissions(self) -> list:
        permission_classes = [IsAuthenticated]
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsAdminUser]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer) -> None:
        """Create notice for support service when created new message from customer."""
        instance = serializer.save()
        customer_created_message_notification(instance)

    def destroy(self, request, *args, **kwargs) -> Response:
        """Delete message. Allowed only for owner of message or admin."""
        instance = self.get_object()
        if self.request.user == instance.author or self.request.user.is_staff:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            status=status.HTTP_403_FORBIDDEN,
            data={'detail': 'You do not have permission to perform this action.'}
        )
