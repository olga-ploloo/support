from user.exections import BlacklistedTokenException
from user.utils.connection import get_redis_client


def check_blacklisted_token(token):
    redis_client = get_redis_client()
    if redis_client.sismember('blacklisted_jwt_tokens', token):
        raise BlacklistedTokenException()


def get_token_from_header(request) -> str:
    raw_token = request.headers.get("Authorization", None)
    if raw_token:
        return raw_token.split()[1]
