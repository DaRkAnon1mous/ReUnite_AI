from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv
load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

client.delete_collection("faces_collection")
print("Deleted collection faces_collection")
collections = client.get_collections()
print("Available collections:", [c.name for c in collections.collections])
