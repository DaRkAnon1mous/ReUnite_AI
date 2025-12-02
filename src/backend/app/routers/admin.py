from fastapi import APIRouter, HTTPException, Depends, Path
from fastapi.security import APIKeyHeader
from ..config import ADMIN_TOKEN
from ..services.db_service import AsyncSessionLocal
from src.backend.db_files.models import Registration, Person
from ..services.embedder import compute_embedding_from_bgr
from ..services.cloudinary_services import upload_image_fileobj
from ..services.qdrant_service import upsert_point
import requests, cv2, numpy as np
from sqlalchemy import select
import json
import uuid
from datetime import datetime 
from ..pipeline import extract_embedding

router = APIRouter()
api_key_header = APIKeyHeader(name="x-admin-token", auto_error=False)

async def admin_required(header: str = Depends(api_key_header)):
    if header != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@router.get("/admin/dashboard")
async def admin_dashboard(_=Depends(admin_required)):
    async with AsyncSessionLocal() as session:
        stmt = select(Registration).where(Registration.status == "pending")
        res = await session.execute(stmt)
        rows = res.scalars().all()
        out = []
        for r in rows:
            out.append({
                "id": str(r.id),
                "person_image_url": r.person_image_url,
                "person_data": json.loads(r.person_data),
                "submitted_at": r.submitted_at.isoformat() if r.submitted_at else None
            })
        return {"pending": out}

@router.post("/admin/verify/{registration_id}")
async def admin_verify(registration_id: str = Path(...), approve: bool = True, _=Depends(admin_required)):
    async with AsyncSessionLocal() as session:
        stmt = select(Registration).where(Registration.id == registration_id)
        res = await session.execute(stmt)
        reg = res.scalar_one_or_none()
        if not reg:
            raise HTTPException(status_code=404, detail="Registration not found")

        if not approve:
            reg.status = "rejected"
            reg.reviewed_at = datetime.utcnow()
            await session.commit()
            return {"status": "rejected"}

        # Approve: convert registration to Person
        pdata = json.loads(reg.person_data)
        image_url = reg.person_image_url

        # download image bytes to compute embedding
        resp = requests.get(image_url)
        arr = np.frombuffer(resp.content, np.uint8)
        img_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)

        embedding = extract_embedding(img_bgr)
        if embedding is None:
            raise HTTPException(status_code=500, detail="Embedding failed")

        person = Person(
            id=uuid.uuid4(),
            name=pdata.get("name"),
            age=pdata.get("age"),
            gender=pdata.get("gender"),
            last_seen_location=pdata.get("last_seen_location"),
            last_seen_date=pdata.get("last_seen_date"),
            last_seen_time=pdata.get("last_seen_time"),
            contact_info=pdata.get("contact_info"),
            additional_details=pdata.get("additional_details"),
            case_id=f"REG{str(uuid.uuid4())[:8]}",
            case_status="active",
            image_url=image_url,
            verified=True
        )
        session.add(person)
        await session.commit()
        await session.refresh(person)

        # Insert embedding to Qdrant using person.id
        upsert_point(str(person.id), embedding, {"person_id": str(person.id), "verified": True, "image_url": image_url})

        # update registration status
        reg.status = "approved"
        reg.reviewed_by = "admin"
        reg.reviewed_at = datetime.utcnow()
        await session.commit()
        return {"status": "approved", "person_id": str(person.id)}
