import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework import status

from ticket.models import Ticket


@pytest.mark.django_db
def test_permissions_tickets_list(auth_client, auth_support_client):
    client = Client()

    assert client.get('/tickets/').status_code == status.HTTP_401_UNAUTHORIZED
    assert auth_client.get('/tickets/').status_code == status.HTTP_403_FORBIDDEN
    assert auth_support_client.get('/tickets/').status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_unsolved_tickets_list(auth_client, auth_support_client):
    client = Client()

    assert client.get('/tickets/unsolved_tickets/').status_code == status.HTTP_401_UNAUTHORIZED
    assert auth_client.get('/tickets/unsolved_tickets/').status_code == status.HTTP_403_FORBIDDEN
    assert auth_support_client.get('/tickets/unsolved_tickets/').status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_customer_tickets_list(client, auth_client, auth_support_client):
    assert client.get('/tickets/customer_own_tickets/').status_code == status.HTTP_403_FORBIDDEN
    assert auth_client.get('/tickets/customer_own_tickets/').status_code == status.HTTP_200_OK
    assert auth_support_client.get('/tickets/customer_own_tickets/').status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_support_tickets_list(auth_client, auth_support_client):
    client = Client()

    assert client.get('/tickets/support_own_tickets/').status_code == status.HTTP_401_UNAUTHORIZED
    assert auth_client.get('/tickets/support_own_tickets/').status_code == status.HTTP_403_FORBIDDEN
    assert auth_support_client.get('/tickets/support_own_tickets/').status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_ticket(client, auth_client, auth_support_client):
    assert client.post('/tickets/', {'description': 'test description'}).status_code == status.HTTP_403_FORBIDDEN
    assert auth_client.post('/tickets/', {'description': 'test description'}).status_code == status.HTTP_201_CREATED
    assert auth_support_client.post('/tickets/',
                                    {'description': 'test description'}).status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_update_ticket(auth_client, auth_support_client):
    user = get_user_model().objects.get(email='support@support.com')
    ticket = Ticket.objects.create(
        description='test description',
        author_id=user.id
    )

    assert auth_support_client.put(f'/tickets/{ticket.id}/', {'status': 'solved'}).status_code == status.HTTP_200_OK
    assert auth_client.put(f'/tickets/{ticket.id}/', {'status': 'solved'}).status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_destroy_ticket(auth_client, auth_support_client):
    user = get_user_model().objects.get(email='testemail@test.com')
    ticket = Ticket.objects.create(
        description='test description',
        author_id=user.id
    )

    assert auth_client.delete(f'/tickets/{ticket.id}/').status_code == status.HTTP_204_NO_CONTENT
    assert auth_support_client.delete(f'/tickets/{ticket.id}/').status_code == status.HTTP_403_FORBIDDEN
