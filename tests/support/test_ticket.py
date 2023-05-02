import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from ticket.models import Ticket


@pytest.mark.django_db
def test_create_ticket(auth_client):
    response = auth_client.post('/tickets/', {'description': 'test description'})
    ticket_from_db = Ticket.objects.first()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['id'] == ticket_from_db.id
    assert response.data['author'] == ticket_from_db.author.username
    assert response.data['description'] == ticket_from_db.description


@pytest.mark.django_db
def test_get_tickets_list(auth_support_client, auth_client):
    user = get_user_model().objects.get(email='testemail@test.com')
    Ticket.objects.bulk_create([
        Ticket(description='test description1',
               author_id=user.id),
        Ticket(description='test description2',
               author_id=user.id)
    ])
    response = auth_support_client.get('/tickets/')
    tickets_from_db = Ticket.objects.all()

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == tickets_from_db.count()


@pytest.mark.django_db
def test_update_ticket(auth_client, auth_support_client, ticket):
    assert auth_support_client.put(f'/tickets/{ticket.id}/', {'status': 'solved'}).status_code == status.HTTP_200_OK
    assert auth_client.put(f'/tickets/{ticket.id}/', {'status': 'solved'}).status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_destroy_ticket(auth_client, auth_support_client, ticket):
    assert auth_client.delete(f'/tickets/{ticket.id}/').status_code == status.HTTP_204_NO_CONTENT
    assert auth_support_client.delete(f'/tickets/{ticket.id}/').status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_permissions_tickets_list(auth_client, auth_support_client):
    client = APIClient()
    assert client.get('/tickets/').status_code == status.HTTP_401_UNAUTHORIZED
    assert auth_client.get('/tickets/').status_code == status.HTTP_403_FORBIDDEN
    assert auth_support_client.get('/tickets/').status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_permissions_unsolved_tickets_list(auth_client, auth_support_client):
    client = APIClient()
    assert client.get('/tickets/unsolved_tickets/').status_code == status.HTTP_401_UNAUTHORIZED
    assert auth_client.get('/tickets/unsolved_tickets/').status_code == status.HTTP_403_FORBIDDEN
    assert auth_support_client.get('/tickets/unsolved_tickets/').status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_permissions_customer_tickets_list(client, auth_client, auth_support_client):
    assert client.get('/tickets/customer_own_tickets/').status_code == status.HTTP_403_FORBIDDEN
    assert auth_client.get('/tickets/customer_own_tickets/').status_code == status.HTTP_200_OK
    assert auth_support_client.get('/tickets/customer_own_tickets/').status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_permissions_support_tickets_list(auth_client, auth_support_client):
    client = APIClient()
    assert client.get('/tickets/support_own_tickets/').status_code == status.HTTP_401_UNAUTHORIZED
    assert auth_client.get('/tickets/support_own_tickets/').status_code == status.HTTP_403_FORBIDDEN
    assert auth_support_client.get('/tickets/support_own_tickets/').status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_permissions_create_ticket(client, auth_client, auth_support_client):
    assert client.post('/tickets/', {'description': 'test description'}).status_code == status.HTTP_403_FORBIDDEN
    assert auth_client.post('/tickets/', {'description': 'test description'}).status_code == status.HTTP_201_CREATED
    assert auth_support_client.post('/tickets/',
                                    {'description': 'test description'}).status_code == status.HTTP_403_FORBIDDEN
