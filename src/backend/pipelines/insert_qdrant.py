from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
from dotenv import load_dotenv

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

def insert_embedding(person_id, embedding, payload):
    client.upsert(
        collection_name="faces_collection",
        points=[
            models.PointStruct(
                id=person_id,
                vector=embedding,
                payload=payload
            )
        ]
    )

def count_points():
    info = client.count("faces_collection")
    return info.count
