from django_redis import get_redis_connection
from django.conf import settings
from redis.client import StrictRedis
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import UntypedToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication

# class BlacklistMiddleware(JWTAuthentication):
#     def __init__(self, get_response):
#         self.get_response = get_response
#         super().__init__()
#
#     def __call__(self, request):
#         if settings.JWT_BLACKLIST_ENABLE:
#             try:
#                 token = self.get_validated_token(request)
#             except InvalidToken:
#                 # If the token is invalid, continue processing the request
#                 pass
#             else:
#                 if self.token_blacklisted(token):
#                     raise InvalidToken('Token is blacklisted')
#
#         response = self.get_response(request)
#
#         return response
#
#     def token_blacklisted(self, token):
#         jti = token['jti']
#         cache_key = settings.JWT_BLACKLIST_CACHE_PREFIX + jti
#         redis_conn = get_redis_connection('default')
#         return redis_conn.get(cache_key) is not None
#
#
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

from user import utils


class BlacklistedTokenException(AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Token is blacklisted'
    default_code = 'token_not_valid'


class BlacklistTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        raw_token = request.headers.get("Authorization", None)
        if raw_token:
            try:
                token = (raw_token.split()[1])
                self.check_blacklisted_token(token)
            except BlacklistedTokenException as error:
                return error
        response = self.get_response(request)
        return response

    def check_blacklisted_token(self, token):
        redis_client = utils.get_redis_client()
        if redis_client.sismember('blacklisted_jwt_tokens', token):
            raise BlacklistedTokenException()
