import jwt
import pytest
from django.conf import settings
from rest_framework import status


@pytest.mark.django_db
def test_register_user(client, test_user_payload):
    response = client.post('/auth/users/', test_user_payload)

    assert response.data['username'] == test_user_payload['username']
    assert response.data['email'] == test_user_payload['email']
    assert 'password' not in response.data


@pytest.mark.django_db
def test_user_creation_fail_if_user_with_email_exist(user, client, test_user_payload):
    payload = dict(
        username='Jon',
        email=test_user_payload['email'],
        password='fhfyy7frn44',
        password2='fhfyy7frn44'
    )
    response = client.post('/auth/users/', payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_access_token_for_user(user, client, test_user_payload):
    response = client.post('/token/', dict(
        email=test_user_payload.get('email'),
        password=test_user_payload.get('password'),
    ))
    access_token = response.data.get('access')
    decoded_data = jwt.decode(jwt=access_token,
                              key=settings.SECRET_KEY,
                              algorithms=["HS256"])

    assert isinstance(decoded_data, dict)
    assert decoded_data['username'] == test_user_payload.get('username')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_access_token_for_user_wrong_password(client, test_user_payload):
    response = client.post('/token/', dict(
        email=test_user_payload.get('email'),
        password='qwert',
    ))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_user_logout(client, auth_client):
    response = auth_client.post('/logout/')

    assert response.status_code == status.HTTP_204_NO_CONTENT



# @pytest.mark.django_db
# def test_activation_url(user, client):
#     # activation_url = reverse('activation')
#     activation_url = settings.DJOSER.get('ACTIVATION_URL')
#     print('hrer')
#     data = {'uid': str(user.pk), 'token': user.activation_token}
#     response = client.post(activation_url, data)
#     # response = client.post('/token/', dict(
#     #     email=test_user.get('email'),
#     #     password='qwert',
#     # ))
#
#     assert response.status_code == status.HTTP_204_NO_CONTENT
#     # assert User.objects.get(pk=user.pk).is_active is True