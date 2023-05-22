import pytest
from rest_framework import status
from rest_framework.test import APIClient

from backend.message.models import Message


@pytest.mark.django_db
def test_create_message(auth_client, ticket):
    response = auth_client.post('/messages/', {
        'ticket': ticket.id,
        'message': 'test message'
    })
    message_from_db = Message.objects.first()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['id'] == message_from_db.id
    assert response.data['ticket'] == message_from_db.ticket.id
    assert response.data['author'] == message_from_db.author.username
    assert response.data['message'] == message_from_db.message


@pytest.mark.django_db
def test_permissions_create_message_authenticated_user(ticket, auth_client, auth_support_client):
    client = APIClient()
    assert client.post('/messages/', {'ticket': ticket.id,
                                      'message': 'test message'}).status_code == status.HTTP_401_UNAUTHORIZED
    assert auth_client.post('/messages/', {'ticket': ticket.id,
                                           'message': 'test message'}).status_code == status.HTTP_201_CREATED
    assert auth_support_client.post('/messages/', {'ticket': ticket.id,
                                                   'message': 'test message'}).status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_destroy_message(auth_client, ticket):
    assert auth_client.delete(f'/messages/{ticket.id}/').status_code == status.HTTP_204_NO_CONTENT
