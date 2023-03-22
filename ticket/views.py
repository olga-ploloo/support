from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from .tasks import send_email
from user.permissions import IsSupport, IsCustomer
from .models import Ticket
from .serializers import TicketSerializer


class TicketViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
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
        if self.action in ['create', 'get_own_tickets']:
            permission_classes = [IsAuthenticated, IsCustomer]
        if self.action in ['list', 'update']:
            permission_classes = [IsAuthenticated, IsSupport]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
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
