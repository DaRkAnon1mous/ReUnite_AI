from qdrant_client import QdrantClient
from qdrant_client.http import models
from ..config import QDRANT_URL, QDRANT_API_KEY
import os

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, prefer_grpc=False)

COLLECTION = "faces_collection"

def search_vectors(embedding, top_k=5, filter_payload=None):
    """
    embedding: list[float]
    filter_payload: dict (e.g., {"verified": True})
    returns list of hits with id, score (distance) and payload
    """
    from qdrant_client.http.models import Filter, FieldCondition, MatchValue
    qfilter = None
    if filter_payload:
        # Build AND filters for matching payloads (simple)
        must = []
        for k, v in filter_payload.items():
            must.append(FieldCondition(key=k, match=MatchValue(value=v)))
        qfilter = Filter(must=must)


    res = client.search(
        collection_name=COLLECTION,
        query_vector=embedding,
        limit=top_k,
        with_payload=True,
        with_vectors=False,
        query_filter=qfilter
    )
    return res

def upsert_point(point_id, embedding, payload):
    client.upsert(
        collection_name=COLLECTION,
        points=[models.PointStruct(id=point_id, vector=embedding, payload=payload)]
    )
