# src/backend/app/services/redis_service.py
import redis
import os
from ..config import REDIS_URL, REDIS_TOKEN

# Upstash works with username/password auth
# redis-py automatically handles this with from_url
redis_client = redis.from_url(
    REDIS_URL,
    password=REDIS_TOKEN,
    decode_responses=True
)

def ping_redis():
    try:
        return redis_client.ping()
    except Exception as e:
        print("Redis connection failed:", e)
        return False
