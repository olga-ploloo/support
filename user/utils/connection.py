import redis


def get_redis_client():
    redis_client = redis.Redis(host='redis', port=6379)
    return redis_client


def add_token_to_blacklist(token):
    redis_instance = get_redis_client()
    redis_instance.sadd("blacklisted_jwt_tokens", str(token))
