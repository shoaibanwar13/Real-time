import os
import redis

# Initialize Redis client
REDIS_URL =  "redis://red-ctufmpl2ng1s739dlicg:6379"
redis_client = redis.from_url(REDIS_URL)

def set_key(key, value, expire=None):
    """
    Set a key-value pair in Redis with optional expiration.
    """
    if expire:
        redis_client.set(key, value, ex=expire)
    else:
        redis_client.set(key, value)

def get_key(key):
    """
    Get a value from Redis by key.
    """
    value = redis_client.get(key)
    return value.decode("utf-8") if value else None
