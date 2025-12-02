from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from ..services.detector import detect_faces
# from ..services.embedder import compute_embedding_from_bgr
from ..services.qdrant_service import search_vectors
from ..services.cloudinary_services import upload_image_fileobj
from ..config import TOP_K, SIMILARITY_THRESHOLD
from ..pipeline import extract_embedding
import cv2
import numpy as np
from ..services.db_service import AsyncSessionLocal
from src.backend.db_files.models import Person
from sqlalchemy import select

router = APIRouter()

@router.post("/search")
async def search_image(file: UploadFile = File(...)):
    contents = await file.read()
    # decode to numpy
    nparr = np.frombuffer(contents, np.uint8)
    img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img_bgr is None:
        raise HTTPException(status_code=400, detail="Invalid image")

    # Detect faces
    dets = detect_faces(img_bgr)
    if not dets:
        raise HTTPException(status_code=404, detail="No face found")

    # Use largest detection
    best = max(dets, key=lambda d: d["box"][2] * d["box"][3])
    x, y, w, h = best["box"]
    x, y = max(0, x), max(0, y)
    face = img_bgr[y:y+h, x:x+w]

    # Compute embedding
    embedding = extract_embedding(face)
    if embedding is None:
        raise HTTPException(status_code=500, detail="No face detected")

    # Query Qdrant (filter only verified entries)
    hits = search_vectors(embedding, top_k=TOP_K, filter_payload={"verified": True})

    results = []
    async with AsyncSessionLocal() as session:
        for h in hits:
            # h.id is person_id if inserted like that
            person_id = h.id
            # convert distance -> similarity (for cosine distance: similarity = 1 - distance)
            # Qdrant returns distance depending on metric; we assume cosine
            dist = h.score
            similarity = 1.0 - dist
            if similarity < SIMILARITY_THRESHOLD:
                continue
            # fetch metadata
            stmt = select(Person).where(Person.id == person_id)
            row = await session.execute(stmt)
            person = row.scalar_one_or_none()
            if not person:
                continue
            results.append({
                "person_id": str(person.id),
                "similarity": float(similarity),
                "image_url": person.image_url,
                "name": person.name,
                "age": person.age,
                "last_seen_location": person.last_seen_location,
                "case_id": person.case_id
            })

    return {"matches": results}
