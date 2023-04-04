from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase

from .serializers import MyTokenObtainPairSerializer, UserLogoutSerialiser
from .utils.connection import add_token_to_blacklist


class UserLogoutView(GenericAPIView):
    serializer_class = UserLogoutSerialiser
    queryset = []

    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        token = request.headers.get("Authorization", None)
        if token:
            try:
                add_token_to_blacklist(token.split()[1])
            except (InvalidToken, TokenError):
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(status=status.HTTP_204_NO_CONTENT)


class MyTokenObtainPairView(TokenObtainPairView):
    """ Check email and password and return an access_token token and refresh_token. """
    serializer_class = MyTokenObtainPairSerializer
