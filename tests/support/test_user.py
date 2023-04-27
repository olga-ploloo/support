import pytest
import jwt
from django.conf import settings

test_user = dict(
        username='testusername',
        email='testemail@test.com',
        password='testpassword',
        password2='testpassword'
    )


@pytest.mark.django_db
def test_register_user(client):
    response = client.post('/auth/users/', test_user)

    assert response.data['username'] == test_user['username']
    assert response.data['email'] == test_user['email']
    assert 'password' not in response.data


@pytest.mark.django_db
def test_user_creation_fail_if_user_with_email_exist(user, client):
    payload = dict(
        username='Jon',
        email='testemail@test.com',
        password='fhfyy7frn44',
        password2='fhfyy7frn44'
    )
    response = client.post('/auth/users/', payload)

    assert response.status_code == 400


@pytest.mark.django_db
def test_create_access_token_for_user(user, client):
    response = client.post('/token/', dict(
        email=test_user.get('email'),
        password=test_user.get('password'),
    ))
    access_token = response.data.get('access')
    decoded_data = jwt.decode(jwt=access_token,
                              key=settings.SECRET_KEY,
                              algorithms=["HS256"])

    assert isinstance(decoded_data, dict)
    assert decoded_data['username'] == test_user.get('username')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_access_token_for_user_wrong_password(client):
    response = client.post('/token/', dict(
        email=test_user.get('email'),
        password='qwert',
    ))

    assert response.status_code == 401


@pytest.mark.django_db
def test_user_logout(client, auth_client):
    response = auth_client.post('/logout/')

    assert response.status_code == 204
