import pytest


@pytest.mark.django_db
def test_register_user(client):
    payload = dict(
        username='testusername',
        email='testemail@test.com',
        password='testpassword',
        password2='testpassword'
    )
    response = client.post('/register/', payload)

    assert response.data['username'] == payload['username']
    assert response.data['email'] == payload['email']
    assert 'password' not in response.data


@pytest.mark.django_db
def test_user_creation_fail_if_user_with_email_exist(self):
    pass


@pytest.mark.django_db
def test_login_user(user, client):
    response = client.post('/login/', dict(
        email='testemail@test.com',
        password='testpassword',
    ))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_user_fail(client):
    response = client.post('/login/', dict(
        email='testemail@test.com',
        password='qwert',
    ))
    assert response.status_code == 400
