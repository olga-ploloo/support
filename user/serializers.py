from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from .models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
                                     # validators=[validate_password]
                                     )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'password2'
        )
        extra_kwargs = {
            'username':
                {'required': True},
            'email':
                {'required': True},
        }

    def create(self, validated_data):
        validated_data.pop('password2')
        auth_user = User.objects.create_user(**validated_data)
        return auth_user

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User


    def validate(self, data):
        user = authenticate(
            email=data['email'],
            password=data['password']
        )
        if user is None:
            raise serializers.ValidationError("Invalid login credentials")
        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            update_last_login(None, user)
            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'role': user.role,
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'role'
        )