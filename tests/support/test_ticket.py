from django.urls import reverse
from ticket.models import Ticket
from rest_framework.test import APITestCase
from django.test import TestCase, Client


class TicketTestCase(TestCase):

    def test_list_tickets_view_performance(self):
        client = Client()
        Ticket.objects.create(
            description='testing message',
            author_id=8
        )
        with self.assertNumQueries(1):
            response = client.get("/tickets/")
        self.assertEqual(response.context["tickets"], 1)
