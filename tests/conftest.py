import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


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
def auth_client(user, client):
    auth_client.login(username='testusername', password='testemail@test.com')
    return auth_client
