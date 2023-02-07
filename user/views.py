# from .permissions import IsSupport


from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserListSerializer

from .models import User


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        print(request.user)
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            # return Response(serializer.data, status=status.HTTP_200_OK)
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role']
                }
            }

            return Response(response, status=status_code)


#
# class UserListView(APIView):
#     serializer_class = UserListSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         # user = request.user
#         # if user.role != 1:
#         #     response = {
#         #         'success': False,
#         #         'status_code': status.HTTP_403_FORBIDDEN,
#         #         'message': 'You are not authorized to perform this action'
#         #     }
#         #     return Response(response, status.HTTP_403_FORBIDDEN)
#         # else:
#
#         users = User.objects.all()
#         serializer = self.serializer_class(users, many=True)
#         response = {
#             'success': True,
#             'status_code': status.HTTP_200_OK,
#             'message': 'Successfully fetched users',
#             'users': serializer.data
#
#         }
#         return Response(response, status=status.HTTP_200_OK)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    # def list(self, request):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     print(request.user)
    #     return Response(serializer.data)
