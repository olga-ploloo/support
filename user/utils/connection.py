import os

import redis


def get_redis_client():
    return redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=int(os.getenv('REDIS_PORT')),
        db=int(os.getenv('REDIS_JWT_BLACKLIST_DB'))
    )
