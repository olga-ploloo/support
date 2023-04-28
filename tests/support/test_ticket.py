import pytest
from django.urls import reverse
from rest_framework import status

from ticket.models import Ticket, AssignTicket
from user.models import User
from rest_framework.test import APITestCase
from django.test import TestCase, Client


#
# class TicketTestCase(TestCase):
#
#     def test_list_tickets_view_performance(self):
#         psss
#         # client = Client()
# user = User.objects.create(
#     username='testusername',
#     email='testemail@test.com',
#     password='testpassword',
#     # password2='testpassword'
# )
# ticket = Ticket.objects.create(
#     description='testing ticket',
#     author=user
# )
# # AssignTicket.objects.create(
# #     ticket=ticket,
# # )
# with self.assertNumQueries(1):
#     response = client.get("/tickets/")
# self.assertEqual(response.context["tickets"], 1)

# @pytest.mark.django_db
# def test_register_user(client):
#     response = client.post('/auth/users/', test_user)
#
#     assert response.data['username'] == test_user['username']
#     assert response.data['email'] == test_user['email']
#     assert 'password' not in response.data


@pytest.mark.django_db
def test_permissions_tickets_list(client, auth_client, auth_support_client):
    # assert client.get('/tickets/').status_code == status.HTTP_403_FORBIDDEN
    assert auth_client.get('/tickets/').status_code == status.HTTP_403_FORBIDDEN
    assert auth_support_client.get('/tickets/').status_code == status.HTTP_200_OK


# @pytest.mark.django_db
# def test_permissions_create_ticket(client, auth_client, auth_support_client):
#     assert client.post('/tickets/').status_code == status.HTTP_403_FORBIDDEN
#     assert auth_client.post('/tickets/').status_code == status.HTTP_403_FORBIDDEN
#     assert auth_support_client.post('/tickets/').status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_permissions_customer_tickets_list(client, auth_client, auth_support_client):
    assert client.get('/tickets/customer_own_tickets/').status_code == status.HTTP_403_FORBIDDEN
    assert auth_client.get('/tickets/customer_own_tickets/').status_code == status.HTTP_200_OK
    assert auth_support_client.get('/tickets/customer_own_tickets/').status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_permissions_support_tickets_list(client, auth_client, auth_support_client):
    # assert client.get('/tickets/support_own_tickets/').status_code == status.HTTP_403_FORBIDDEN
    assert auth_client.get('/tickets/support_own_tickets/').status_code == status.HTTP_403_FORBIDDEN
    assert auth_support_client.get('/tickets/support_own_tickets/').status_code == status.HTTP_200_OK
