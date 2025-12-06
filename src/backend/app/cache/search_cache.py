import hashlib
import json
from ..services.redis_service import redis_client

SEARCH_TTL = 60 * 60 * 3  # 3 hours

def hash_embedding(embedding):
    e = ",".join([f"{x:.5f}" for x in embedding])
    return hashlib.sha256(e.encode()).hexdigest()

def get_cached_search(embedding):
    key = f"search:{hash_embedding(embedding)}"
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    return None

def set_cached_search(embedding, results):
    key = f"search:{hash_embedding(embedding)}"
    redis_client.set(key, json.dumps(results), ex=SEARCH_TTL)
