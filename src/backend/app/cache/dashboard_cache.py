# src/backend/app/cache/dashboard_cache.py
import json
from ..services.redis_service import redis_client

DASHBOARD_TTL = 30  # seconds

def get_dashboard_cache():
    data = redis_client.get("dashboard")
    if data:
        return json.loads(data)
    return None

def set_dashboard_cache(payload):
    redis_client.set("dashboard", json.dumps(payload), ex=DASHBOARD_TTL)

def clear_dashboard_cache():
    redis_client.delete("dashboard")
