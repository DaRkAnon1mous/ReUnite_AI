import hashlib
import json
from ..services.redis_service import redis_client

EMBEDDING_TTL = 60 * 60 * 24  # 24 hours

def compute_hash(image_bytes: bytes):
    return hashlib.sha256(image_bytes).hexdigest()

def get_cached_embedding(image_bytes: bytes):
    key = f"embed:{compute_hash(image_bytes)}"
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def set_cached_embedding(image_bytes: bytes, embedding):
    key = f"embed:{compute_hash(image_bytes)}"
    redis_client.set(key, json.dumps(embedding), ex=EMBEDDING_TTL)
