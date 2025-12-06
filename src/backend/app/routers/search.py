from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from ..services.detector import detect_faces
# from ..services.embedder import compute_embedding_from_bgr
from ..services.qdrant_service import search_vectors
from ..services.cloudinary_services import upload_image_fileobj
from ..config import TOP_K, SIMILARITY_THRESHOLD
from ..pipeline import extract_embedding
import cv2
import numpy as np
from ..schemas import SearchResponse, MatchItem
from ..cache.person_cache import get_person_metadata, cache_person_metadata
from ..cache.embedding_cache import get_cached_embedding, set_cached_embedding
from ..cache.search_cache import get_cached_search, set_cached_search
from ..services.db_service import AsyncSessionLocal
from src.backend.db_files.models import Person
from sqlalchemy import select

router = APIRouter()

@router.post("/search", response_model=SearchResponse)
async def search_image(file: UploadFile = File(...)):
    # Step 1 — read file
    img_bytes = await file.read()

    # Step 2 — decode image
    nparr = np.frombuffer(img_bytes, np.uint8)
    img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img_bgr is None:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Step 3 — embedding cache
    embedding = get_cached_embedding(img_bytes)
    if embedding is None:
        embedding = extract_embedding(img_bgr)
        if embedding is None:
            raise HTTPException(status_code=400, detail="No face detected")
        set_cached_embedding(img_bytes, embedding)

    # Step 4 — search cache
    cached = get_cached_search(embedding)
    if cached:
        return SearchResponse(matches=cached)

    # Step 5 — query Qdrant
    hits = search_vectors(embedding, top_k=TOP_K, filter_payload={"verified": True})
    print("DEBUG HIT SAMPLE:", hits[0].__dict__)
    if not hits:
        return SearchResponse(matches=[])

    # Step 6 — join with Postgres metadata
    matches = []
    async with AsyncSessionLocal() as session:
        for h in hits:
            print("PAYLOAD:", h.payload)
            pid = (
                    h.payload.get("person_id") 
                    or h.payload.get("id") 
                    or h.payload.get("personId")
                )

            if not pid:
                print("⚠ Skipping hit — no person_id in payload:", h.payload)
                continue

            # try metadata cache
            metadata = get_person_metadata(pid)
            if metadata is None:
                # fetch from Postgres
                stmt = select(Person).where(Person.id == pid)
                res = await session.execute(stmt)
                p = res.scalar_one_or_none()
                if not p:
                    continue

                metadata = {
                    "person_id": pid,
                    "name": p.name,
                    "age": p.age,
                    "image_url": p.image_url,
                    "last_seen_location": p.last_seen_location,
                    "case_id": p.case_id,
                }
                cache_person_metadata(pid, metadata)

            similarity =  h.score  # Qdrant returns distance, convert to similarity
            print("RAW QDRANT SCORE:", h.score)
            print("CONVERTED SIMILARITY:", similarity)
            if similarity >= SIMILARITY_THRESHOLD:
                matches.append(
                    MatchItem(
                        person_id=metadata["person_id"],
                        similarity=float(similarity),
                        image_url=metadata["image_url"],
                        name=metadata.get("name"),
                        age=metadata.get("age"),
                        last_seen_location=metadata.get("last_seen_location"),
                        case_id=metadata.get("case_id"),
                    )
                )

    # Step 7 — cache results
    results_payload = [m.dict() for m in matches]
    set_cached_search(embedding, results_payload)

    return SearchResponse(matches=matches)