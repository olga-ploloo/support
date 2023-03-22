import os
from django.core.cache import cache
import redis
from datetime import datetime, timedelta
from django.conf import settings


def get_redis_client():
    # return redis.from_url(os.getenv('JWT_BLACKLIST_TOKENS_CACHE'))
    # redis_client = redis.StrictRedis(host='redis', port=6379, db=4)
    redis_client = redis.Redis(host='redis', port=6379)


    return redis_client


def add_token_to_blacklist(token):
    # cache.add('blacklisted', token )
    # Получаем идентификатор JWT токена
    # jti = token["jti"]
    # Добавляем идентификатор в Redis
    # expiration_time = datetime.utcfromtimestamp(token["exp"])
    # remaining_time = expiration_time - datetime.utcnow()
    redis_instance = get_redis_client()
    redis_instance.sadd("blacklisted_jwt_tokens", str(token))
