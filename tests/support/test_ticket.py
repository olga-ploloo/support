from django.urls import reverse
from ticket.models import Ticket, AssignTicket
from user.models import User
from rest_framework.test import APITestCase
from django.test import TestCase, Client


class TicketTestCase(TestCase):

    def test_list_tickets_view_performance(self):
        client = Client()
        user = User.objects.create(
            username='testusername',
            email='testemail@test.com',
            password='testpassword',
            # password2='testpassword'
        )
        ticket = Ticket.objects.create(
            description='testing ticket',
            author=user
        )
        # AssignTicket.objects.create(
        #     ticket=ticket,
        # )
        with self.assertNumQueries(3):
            response = client.get("/assign_ticket/support_own_tickets/")
            # self.assertEqual(response.context["tickets"], 1)




