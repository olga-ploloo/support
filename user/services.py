from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


def authenticate_user(data):
    user = authenticate(
        email=data['email'],
        password=data['password']
    )
    if user is None:
        raise serializers.ValidationError("Invalid login credentials")
    refresh_token, access_token = get_token(user)
    update_last_login(None, user)
    return {
        'access': access_token,
        'refresh': refresh_token,
        'email': user.email,
        'role': user.role,
    }


def get_token(user):
    refresh = RefreshToken.for_user(user)
    refresh_token = str(refresh)
    access_token = str(refresh.access_token)
    return refresh_token, access_token
