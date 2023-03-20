from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase

from .serializers import MyTokenObtainPairSerializer, UserLogoutSerialiser


class UserLogoutView(TokenViewBase):
    serializer_class = UserLogoutSerialiser
    queryset = []
    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MyTokenObtainPairView(TokenObtainPairView):
    """ Check email and password and return an access_token token and refresh_token. """
    serializer_class = MyTokenObtainPairSerializer
