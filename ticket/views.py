from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from user.permissions import IsCustomer, IsSupport

from .models import Ticket
from .serializers import TicketSerializer
from .tasks import send_email


class TicketViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Ticket.objects.prefetch_related('messages')
    serializer_class = TicketSerializer

    def get_queryset(self):
        if self.request.user and self.action == 'get_own_tickets':
            return self.queryset.filter(author=self.request.user)
        return self.queryset

    # only customer
    @action(methods=["get"], detail=False, url_path="own_tickets", url_name="own_tickets")
    def get_own_tickets(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_permissions(self) -> list:
        permission_classes = [IsAuthenticated]
        if self.action in ['create', 'get_own_tickets', 'destroy']:
            permission_classes = [IsAuthenticated, IsCustomer, IsAdminUser]
        if self.action in ['list', 'update']:
            permission_classes = [IsAuthenticated, IsSupport, IsAdminUser]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        instance = serializer.save()
        # make notice for support

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data_to_change = {'status': request.data.get("status")}
        serializer = self.serializer_class(instance, data=data_to_change, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        ticket = serializer.save()
        send_email.delay(ticket.id)

    # only owner of ticket or admin can delete ticket
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user == instance.author or self.request.user.is_staff:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            status=status.HTTP_403_FORBIDDEN,
            data={'detail': 'You do not have permission to perform this action.'}
        )
