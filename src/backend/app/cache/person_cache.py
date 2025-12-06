# src/backend/app/cache/person_cache.py
import json
from ..services.redis_service import redis_client

METADATA_TTL = 60 * 60 * 6  # 6 hours

def cache_person_metadata(person_id: str, metadata: dict):
    key = f"person:{person_id}"
    redis_client.set(key, json.dumps(metadata), ex=METADATA_TTL)

def get_person_metadata(person_id: str):
    key = f"person:{person_id}"
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def invalidate_person_metadata(person_id: str):
    key = f"person:{person_id}"
    redis_client.delete(key)
