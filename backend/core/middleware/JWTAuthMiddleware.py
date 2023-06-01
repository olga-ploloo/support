from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


@database_sync_to_async
def get_user(user_id) -> User:
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return AnonymousUser()


def decode_token(token) -> int | None:
    try:
        decoded_token = AccessToken(token)
        return decoded_token['user_id']
    except (InvalidToken, TokenError):
        return None


class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"])
        if b'token' in query_string:
            token = query_string[b'token'][0].decode()
            user_id = decode_token(token)
            scope['user'] = await get_user(user_id)
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)


JwtAuthMiddlewareStack = lambda inner: JwtAuthMiddleware(AuthMiddlewareStack(inner))
