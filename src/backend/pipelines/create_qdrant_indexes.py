from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import os

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    prefer_grpc=False
)

COLLECTION = "faces_collection"

print("➡ Creating index for payload field: verified (bool) ...")

client.create_payload_index(
    collection_name=COLLECTION,
    field_name="verified",
    field_type="bool"
)

print("✓ Index created successfully!")
