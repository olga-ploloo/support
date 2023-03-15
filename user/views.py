from django.contrib.auth.models import update_last_login
from rest_framework import status, viewsets, mixins, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from . import services
from .serializers import UserRegistrationSerializer, UserListSerializer, UserLoginSerializer
from .models import User


class UserRegistrationViewSet(mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    """Create new user."""
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)


class UserLoginViewSet(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    """ Check email and password and return an access_token token, refresh_token, email and role. """
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh_token, access_token = services.get_token_for_user(user)
        update_last_login(None, user)
        return Response({
            'refresh_token': refresh_token,
            'access_token': access_token,
            'email': user.email,
            'role': user.role,
        }, status=status.HTTP_200_OK)


class UserLogoutView(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'message': 'Logout successful.'}, status=204)
            except Exception as e:
                return Response({'error': str(e)}, status=400)
        else:
            return Response({'error': 'Refresh token is required.'}, status=400)


class UserViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)
