from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from user.permissions import IsCustomer, IsSupport

from .models import Ticket
from .serializers import TicketSerializer
from .services import status_update_notification, new_ticket_create_notification


class TicketViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Ticket.objects.select_related('messages')
    serializer_class = TicketSerializer

    def get_queryset(self) -> queryset:
        if self.request.user and self.action == 'get_own_tickets':
            return Ticket.objects.prefetch_related('messages').filter(author=self.request.user)
        if self.action == 'unsolved_tickets':
            return Ticket.objects.prefetch_related('messages').filter(status=Ticket.TicketStatus.UNSOLVED)
        return self.queryset

    @action(methods=["get"], detail=False, url_path="unsolved_tickets", url_name="unsolved_tickets")
    def get_unsolved_tickets(self, request, *args, **kwargs) -> Response:
        """Return all unsolved tickets. Allowed only for support services."""
        return self.list(request, *args, **kwargs)

    @action(methods=["get"], detail=False, url_path="own_tickets", url_name="own_tickets")
    def get_own_tickets(self, request, *args, **kwargs) -> Response:
        """Return list of tickets created by the current user. Allowed only for customers."""
        return self.list(request, *args, **kwargs)

    def get_permissions(self) -> list:
        permission_classes = [IsAuthenticated]
        if self.action in ['create', 'get_own_tickets', 'destroy']:
            permission_classes = [IsAuthenticated, IsCustomer | IsAdminUser]
        if self.action in ['list', 'update', 'unsolved_tickets']:
            permission_classes = [IsAuthenticated, IsSupport | IsAdminUser]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer) -> None:
        """Create notice for support service when created new ticket."""
        instance = serializer.save()
        new_ticket_create_notification(instance)

    def update(self, request, *args, **kwargs) -> Response:
        """Update only ticket status. Allowed only for support services."""
        instance = self.get_object()
        data_to_change = {'status': request.data.get("status")}
        serializer = self.serializer_class(instance, data=data_to_change, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer) -> None:
        """Send email for customer after updating ticket status."""
        ticket = serializer.save()
        status_update_notification(ticket.id)

    def destroy(self, request, *args, **kwargs) -> Response:
        """Delete ticket. Allowed only for owner of ticket or admin."""
        instance = self.get_object()
        if self.request.user == instance.author or self.request.user.is_staff:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            status=status.HTTP_403_FORBIDDEN,
            data={'detail': 'You do not have permission to perform this action.'}
        )
