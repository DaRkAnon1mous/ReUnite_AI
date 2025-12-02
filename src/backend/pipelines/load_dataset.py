import os
import json
import asyncio
from src.backend.pipelines.upload_cloudinary import upload_image
from src.backend.pipelines.compute_embeddings import compute_embedding
from src.backend.pipelines.insert_postgres import insert_metadata
from src.backend.pipelines.insert_qdrant import insert_embedding

IMAGE_DIR = "data/processed"
METADATA_FILE = "data/metadata/persons_metadata.json"

async def load_dataset():
    # Maps filename → Cloudinary URL
    cloudinary_map = {}

    print("STEP 1: Uploading images to Cloudinary...")
    for fname in os.listdir(IMAGE_DIR):
        if fname.endswith(".jpg"):
            path = os.path.join(IMAGE_DIR, fname)
            url = upload_image(path)
            cloudinary_map[fname] = url

    print("STEP 2: Inserting metadata into Postgres...")
    await insert_metadata(METADATA_FILE, cloudinary_map)

    print("STEP 3: Computing embeddings and inserting into Qdrant...")
    with open(METADATA_FILE, "r") as f:
        data = json.load(f)

    for person in data:
        pid = person["id"]
        img_path = os.path.join(IMAGE_DIR, person["image_filename"])

        emb = compute_embedding(img_path)
        if emb is None:
            print(f"No embedding for {img_path}")
            continue

        payload = {
            "id": pid,
            "verified": True,
            "image_url": cloudinary_map[person["image_filename"]],
        }

        insert_embedding(pid, emb, payload)

    print("\n🎉 DONE — Dataset fully loaded into Cloudinary, Postgres & Qdrant!\n")

if __name__ == "__main__":
    asyncio.run(load_dataset())
