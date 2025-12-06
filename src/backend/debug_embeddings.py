# debug_embedding_check.py
import os, json, math
from dotenv import load_dotenv
load_dotenv()

from qdrant_client import QdrantClient
from .app.services.qdrant_service import COLLECTION
from .app.pipeline import extract_embedding
import requests
import numpy as np

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def print_collection_info():
    info = client.get_collection(COLLECTION)
    print("Collection info keys:", list(info.__dict__.keys()) if info else info)
    try:
        cfg = info.result.config
        print("Vectors config:", cfg.vectors)
        print("Distance/metric may be in collection config (check vector params above).")
    except Exception as e:
        print("Could not print config:", e)

def get_one_point():
    # scroll returns (points, next_page_offset) in your version
    points, offset = client.scroll(collection_name=COLLECTION, limit=1)

    if not points or len(points) == 0:
        print("No points in collection.")
        return None

    p = points[0]
    print("Point id:", p.id)

    # Try to fetch full point with vector
    try:
        full = client.get_point(collection_name=COLLECTION, id=p.id, with_vector=True)
        vect = full.vector  # no .result in current API
    except Exception:
        vect = getattr(p, "vector", None) or p.payload.get("vector")
    
    if vect is None:
        print("No vector found for point", p.id)
        return None
    else:
        print("Stored vector length:", len(vect))
        print("Stored vector sample (first 10):", vect[:10])
        return p.id, p.payload, np.array(vect, dtype=float)

    print("Stored vector length:", len(vect))
    print("Stored vector sample (first 10):", vect[:10])
    return p.id, p.payload, np.array(vect, dtype=float)

def compute_embedding_from_image_url(image_url):
    r = requests.get(image_url, timeout=10)
    img_arr = np.frombuffer(r.content, np.uint8)
    import cv2
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    emb = extract_embedding(img)  # pipeline.extract_embedding returns list
    if emb is None:
        print("extract_embedding returned None")
        return None
    emb = np.array(emb, dtype=float)
    print("Fresh embedding length:", emb.shape)
    print("Fresh embedding sample (first 10):", emb[:10])
    return emb

def cosine_sim(a, b):
    a = np.array(a); b = np.array(b)
    return float(np.dot(a,b) / (np.linalg.norm(a)*np.linalg.norm(b)))

if __name__ == "__main__":
    print_collection_info()
    point = get_one_point()
    if not point:
        raise SystemExit(1)
    pid, payload, stored = point
    # try to get image_url from payload or payload keys
    image_url = None
    if payload and isinstance(payload, dict):
        image_url = payload.get("image_url") or payload.get("url") or payload.get("face_url")
    print("Payload keys:", payload.keys() if payload else None)
    print("Image URL found:", image_url)
    if not image_url:
        print("No image_url in payload — please provide one id to test.")
    else:
        fresh = compute_embedding_from_image_url(image_url)
        if fresh is not None:
            print("Cosine similarity stored vs fresh :", cosine_sim(stored, fresh))
