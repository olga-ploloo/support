from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import MyTokenObtainPairSerializer, UserLogoutSerialiser
from .services import add_token_to_blacklist, get_token_from_header


class UserLogoutView(GenericAPIView):
    serializer_class = UserLogoutSerialiser
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        token = get_token_from_header(request)
        if token:
            try:
                add_token_to_blacklist(token)
            except (InvalidToken, TokenError):
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(status=status.HTTP_204_NO_CONTENT)


class MyTokenObtainPairView(TokenObtainPairView):
    """ Check email and password and return an access_token token and refresh_token. """
    serializer_class = MyTokenObtainPairSerializer


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        kwargs['data'] = {'uid': self.kwargs.get('uid'), 'token': self.kwargs.get('token')}

        return serializer_class(*args, **kwargs)

    def activation(self, request, *args, **kwargs):
        super().activation(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
