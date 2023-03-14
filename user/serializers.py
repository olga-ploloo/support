from .models import User
from . import services
from rest_framework import serializers


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


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'refresh', 'access', 'role')

    def create(self, data):
        return services.authenticate_user(data)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'role'
        )
