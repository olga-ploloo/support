import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_register_user():
    payload = dict(
        username='testusername',
        email='testemail1@test.com',
        password='testpassword',
        password2='testpassword'
    )
    response = client.post('/register/', payload)

    assert response.data['username'] == payload['username']
    assert response.data['email'] == payload['email']
    assert 'password' not in response.data


@pytest.mark.django_db
def test_login_user():
    payload = dict(
        username='testusername',
        email='testemail1@test.com',
        password='testpassword',
        password2='testpassword'
    )
    client.post('/register/', payload)
    response = client.post('/login/', dict(
        password='testpassword',
        email='testemail1@test.com',
    ))
    assert response.status_code == 201
