## Run only once

from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
from dotenv import load_dotenv

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

client.recreate_collection(
    collection_name="faces_collection",
    vectors_config=models.VectorParams(
        size=512,
        distance=models.Distance.COSINE
    )
)

print("Created collection faces_collection with vector size 512.")
