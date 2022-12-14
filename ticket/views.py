from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Ticket
from .serializers import TicketSerializer

from rest_framework import viewsets


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated,)