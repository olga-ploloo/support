from django.conf import settings

from user.exceptions import BlacklistedTokenException, InvalidHeadersException
from user.utils.connection import get_redis_client


def check_blacklisted_token(token):
    redis_client = get_redis_client()
    if redis_client.exists(token):
        raise BlacklistedTokenException()


def get_token_from_header(request):
    raw_token = request.headers.get('Authorization', None)
    if raw_token:
        try:
            token = raw_token.split()[1]
        except (IndexError, ValueError):
            raise InvalidHeadersException()
        return token


def add_token_to_blacklist(token):
    redis_instance = get_redis_client()
    redis_instance.set(str(token), "blacklisted_jwt_tokens", ex=settings.JWT_BLACKLIST_REDIS_EXPIRATION)
