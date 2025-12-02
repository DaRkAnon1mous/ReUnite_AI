import json, os, asyncio
from sqlalchemy import insert
from src.backend.db_files.database import AsyncSessionLocal
from src.backend.db_files.models import Person
from datetime import datetime

async def insert_metadata(metadata_file, cloudinary_map):
    with open(metadata_file, "r") as f:
        data = json.load(f)

    async with AsyncSessionLocal() as session:
        for entry in data:
            filename = entry["image_filename"]  # get before deleting

            # --- Transform fields ---
            entry["last_seen_date"] = datetime.strptime(
                entry["last_seen_date"], "%Y-%m-%d"
            ).date()

            entry["last_seen_time"] = datetime.strptime(
                entry["last_seen_time"], "%H:%M"
            ).time()

            # Cloudinary URL
            entry["image_url"] = cloudinary_map[filename]

            # Verified
            entry["verified"] = True

            # qdrant ID (to fill later)
            entry["qdrant_id"] = None

            # Remove fields not in model
            for key in ["image_filename", "is_synthetic", "created_at"]:
                entry.pop(key, None)

            # Insert
            session.add(Person(**entry))

        await session.commit()


if __name__ == "__main__":
    # Later fill cloudinary_map dict
    pass
