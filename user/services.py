from user.exections import BlacklistedTokenException, InvalidHeadersException
from user.utils.connection import get_redis_client


def check_blacklisted_token(token):
    redis_client = get_redis_client()
    if redis_client.sismember('blacklisted_jwt_tokens', token):
        raise BlacklistedTokenException()


def get_token_from_header(request):
    raw_token = request.headers.get('Authorization', None)
    if raw_token:
        try:
            token = raw_token.split()[1]
        except (IndexError, ValueError):
            raise InvalidHeadersException()
        return token
