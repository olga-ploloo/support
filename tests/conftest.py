import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from ticket.models import Ticket


@pytest.fixture
def user():
    user = get_user_model().objects.create_user(
        username='testusername',
        email='testemail@test.com',
        password='testpassword',
    )
    user.is_active = True
    user.save()

    return user


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_client(user):
    auth_client = APIClient()
    token = RefreshToken.for_user(user)
    auth_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')

    return auth_client


@pytest.fixture
def ticket(user):
    user = get_user_model().objects.get(email='testemail@test.com')
    ticket = Ticket.objects.create(
        description='test description',
        author_id=user.id
    )

    return ticket


@pytest.fixture
def support_user():
    user = get_user_model().objects.create_user(
        username='support',
        email='support@support.com',
        password='support',
    )
    user.role = 'support'
    user.is_active = True
    user.save()

    return user


@pytest.fixture
def auth_support_client(support_user, client):
    token = RefreshToken.for_user(support_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')

    return client


@pytest.fixture
def test_user_payload():
    return dict(
        username='testusername',
        email='testemail@test.com',
        password='testpassword',
        password2='testpassword'
    )
