from django.contrib.auth import authenticate
from .models import User
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
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
            'password':
                {
                    'required': True,
                    'write_only': True,
                    # 'validators': [validate_password]
                }
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

    def validate(self, data) -> list:
        user = authenticate(
            email=data['email'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        data['user'] = user
        return data


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'role'
        )
