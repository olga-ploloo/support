from django.shortcuts import render
from rest_framework import generics
from .models import Ticket
from .serializers import TicketSerializer


class TicketApiView(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
