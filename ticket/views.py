from django.core.mail import send_mail
from django.db.models import Prefetch
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import HttpResponse
from rest_framework.response import Response

from user.permissions import IsSupport, IsCustomer
from .models import Ticket
from .serializers import TicketSerializer

from rest_framework import viewsets


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.prefetch_related('messages')
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user and self.action == 'get_own_tickets':
            return self.queryset.filter(author=self.request.user)
        return self.queryset

    # only customer
    @action(methods=["get"], detail=False, url_path="own_tickets", url_name="own_tickets")
    def get_own_tickets(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    # def get_permissions(self):
    #     if self.action == 'create':
    #         permission_classes = [IsCustomer]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]

    # only customer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # make notice for support
        return Response(serializer.data)

    # only support
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data_to_change = {'status': request.data.get("status")}
        serializer = self.serializer_class(instance, data=data_to_change, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
        send_mail(
            'Subject here',
            'Here is the message.',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )
        return Response(serializer.data)