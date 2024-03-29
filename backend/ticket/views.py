from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from backend.user.permissions import IsCustomer, IsSupport

from .models import AssignTicket, Ticket
from .serializers import AssignTicketSerializer, TicketSerializer, TicketCreateSerializer
from .services import status_update_notification


class TicketViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Ticket.objects.select_related('author').select_related('assigned_ticket').prefetch_related('messages')
    serializer_class = TicketSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return TicketCreateSerializer
        return self.serializer_class

    def get_queryset(self) -> queryset:
        if self.action == 'get_unassigned_tickets':
            return self.queryset.filter(assigned_ticket__is_assign=False)
        if self.request.user and self.action == 'get_customer_own_tickets':
            return self.queryset.filter(author=self.request.user)
        if self.request.user and self.action == 'get_support_own_tickets':
            return self.queryset.filter(assigned_ticket__assigned_support=self.request.user)
        return super().get_queryset()

    @action(methods=["get"], detail=False, url_path="unassigned_tickets", url_name="unassigned_tickets")
    def get_unassigned_tickets(self, request, *args, **kwargs) -> Response:
        """Return all unassigned tickets. Allowed only for support services."""
        return self.list(request, *args, **kwargs)

    @action(methods=["get"], detail=False, url_path="customer_own_tickets", url_name="customer_own_tickets")
    def get_customer_own_tickets(self, request, *args, **kwargs) -> Response:
        """Return list of tickets created by the current user. Allowed only for customers."""
        return self.list(request, *args, **kwargs)

    @action(methods=["get"], detail=False, url_path="support_own_tickets", url_name="support_own_tickets")
    def get_support_own_tickets(self, request, *args, **kwargs) -> Response:
        """Return list of tickets assigned to the current support service. Allowed only for support services."""
        return self.list(request, *args, **kwargs)

    # def get_permissions(self) -> list:
    #     permission_classes = [IsAuthenticated]
    #     if self.action in ['create', 'get_customer_own_tickets', 'destroy']:
    #         permission_classes = [IsAuthenticated, IsCustomer | IsAdminUser]
    #     if self.action in ['list', 'update', 'get_unsolved_tickets', 'get_support_own_tickets']:
    #         permission_classes = [IsAuthenticated, IsSupport | IsAdminUser]
    #
    #     return [permission() for permission in permission_classes]

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


class AssignTicketViewSet(mixins.UpdateModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    queryset = AssignTicket.objects.select_related('ticket')
    serializer_class = AssignTicketSerializer
    permission_classes = [IsAuthenticated, IsSupport | IsAdminUser]

    def get_queryset(self) -> queryset:
        if self.action == 'list':
            """Return all unassigned tickets. Allowed only for support services."""
            return self.queryset.filter(is_assign=False)
        return super().get_queryset()

    def perform_update(self, serializer) -> None:
        """initialization ticket: set current support user """
        serializer.save(
            is_assign=True,
            assigned_support=self.request.user
        )


class TicketStatusChoicesListView(APIView):
    """Return the list of allowed statuses for the ticket."""
    def get(self, request):
        choices = Ticket.TicketStatus.choices
        return Response(choices)


class TicketPermissionToChat(APIView):
    """Receive ticket_id and current user_id, check is user owner or assigned support and return bool."""
    def get(self, request) -> Response:
        user_id = request.query_params.get('user_id')
        ticket = Ticket.objects.get(id=request.query_params.get('ticket'))
        if int(user_id) in [ticket.author_id, ticket.assigned_ticket.assigned_support_id]:
            return Response({'allow': True})
        return Response({'allow': False})
