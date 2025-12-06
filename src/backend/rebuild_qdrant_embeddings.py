# rebuild_qdrant_embeddings.py
import os
import json
import asyncio
import numpy as np
import requests
from dotenv import load_dotenv
load_dotenv()

from qdrant_client import QdrantClient
from qdrant_client.http import models
from sqlalchemy import select
from src.backend.app.pipeline import extract_embedding
from src.backend.db_files.models import Person
from src.backend.app.services.db_service import AsyncSessionLocal

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

async def rebuild():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Person))
        persons = result.scalars().all()

        print(f"Found {len(persons)} persons to re-embed\n")

        for p in persons:
            print("Rebuilding:", p.id)

            # Download image
            try:
                resp = requests.get(p.image_url, timeout=10)
                arr = np.frombuffer(resp.content, np.uint8)
                import cv2
                img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            except Exception as e:
                print("❌ Failed to load image:", p.image_url)
                continue

            emb = extract_embedding(img)
            if emb is None:
                print("❌ No face detected for:", p.image_url)
                continue

            # Upsert into Qdrant
            client.upsert(
                collection_name="faces_collection",
                points=[
                    models.PointStruct(
                        id=str(p.id),
                        vector=emb,
                        payload={
                            "person_id": str(p.id),
                            "verified": True,
                            "image_url": p.image_url
                        }
                    )
                ]
            )

        print("\n🎉 DONE — All embeddings regenerated & stored successfully!")

if __name__ == "__main__":
    asyncio.run(rebuild())
