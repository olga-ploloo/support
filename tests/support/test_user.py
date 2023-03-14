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