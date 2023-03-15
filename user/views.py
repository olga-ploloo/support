from django.contrib.auth.models import update_last_login
from rest_framework import status, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from . import services
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserListSerializer
from .models import User


class UserRegistrationViewSet(mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)


class UserLoginViewSet(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    """ Check email and password and return an auth token """
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh_token, access_token = services.get_token(user)
        update_last_login(None, user)
        return Response({
            'refresh_token': refresh_token,
            'access_token': access_token,
            'email': user.email,
            'role': user.role,
        }, status=status.HTTP_200_OK)


class UserViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)
