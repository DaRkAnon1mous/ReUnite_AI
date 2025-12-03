# src/backend/app/routers/admin.py
import json
import uuid
import requests
import numpy as np
import cv2
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from ..auth.clerk_auth import verify_clerk_admin_token
from ..services.db_service import AsyncSessionLocal
from src.backend.db_files.models import Registration, Person
from ..services.qdrant_service import upsert_point
from ..services.cloudinary_services import upload_image_fileobj
from ..services.caseid import generate_next_case_id
from ..pipeline import extract_embedding
from sqlalchemy import select, func
from datetime import datetime

router = APIRouter()

@router.get("/admin/registrations")
async def admin_registrations(_=Depends(verify_clerk_admin_token), limit: int = Query(50)):
    async with AsyncSessionLocal() as session:
        stmt = select(Registration).where(Registration.status == "pending").order_by(Registration.submitted_at.desc()).limit(limit)
        res = await session.execute(stmt)
        regs = res.scalars().all()
        out = []
        for r in regs:
            out.append({
                "registration_id": str(r.id),
                "person_data": json.loads(r.person_data),
                "person_image_url": r.person_image_url,
                "aadhar_image_url": r.aadhar_image_url,
                "submitted_at": r.submitted_at.isoformat() if r.submitted_at else None
            })
        return {"pending": out}

@router.post("/admin/verify/{registration_id}")
async def admin_verify(registration_id: str = Path(...), approve: bool = True, _=Depends(verify_clerk_admin_token)):
    async with AsyncSessionLocal() as session:
        stmt = select(Registration).where(Registration.id == registration_id)
        res = await session.execute(stmt)
        reg = res.scalar_one_or_none()
        if not reg:
            raise HTTPException(status_code=404, detail="Registration not found")

        if not approve:
            # reject
            await session.delete(reg)
            await session.commit()
            return {"status": "rejected"}

        # approve: prepare person data
        pdata = json.loads(reg.person_data)
        image_url = reg.person_image_url

        # Ensure we have embedding: compute from stored image if not available
        # Download image bytes
        try:
            resp = requests.get(image_url, timeout=10)
            resp.raise_for_status()
            arr = np.frombuffer(resp.content, np.uint8)
            img_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to download image: {e}")

        embedding = extract_embedding(img_bgr)
        # if embedding None, we still proceed but point will not be added to Qdrant automatically
        # generate new person id and next case id
        new_person_id = uuid.uuid4()
        case_id = await generate_next_case_id()

        person = Person(
            id=new_person_id,
            name=pdata.get("name"),
            age=pdata.get("age"),
            gender=pdata.get("gender"),
            last_seen_location=pdata.get("last_seen_location"),
            last_seen_date=pdata.get("last_seen_date"),
            last_seen_time=pdata.get("last_seen_time"),
            contact_info=pdata.get("contact_info"),
            additional_details=pdata.get("additional_details"),
            case_id=case_id,
            case_status="active",
            reported_by=pdata.get("reporter") or "Self",
            reporter_contact=pdata.get("reporter_contact"),
            image_url=image_url,
            verified=True
        )
        session.add(person)
        await session.commit()
        await session.refresh(person)

        # upsert embedding to Qdrant (if available)
        if embedding is not None:
            payload = {"person_id": str(person.id), "verified": True, "image_url": image_url}
            upsert_point(str(person.id), embedding, payload)

        # delete registration
        await session.delete(reg)
        await session.commit()

        return {"status": "approved", "person_id": str(person.id)}

@router.get("/admin/dashboard")
async def admin_dashboard(_=Depends(verify_clerk_admin_token)):
    async with AsyncSessionLocal() as session:
        # counts
        total_stmt = select(func.count()).select_from(Person)
        total_res = await session.execute(total_stmt)
        total_persons = total_res.scalar_one()

        verified_stmt = select(func.count()).select_from(Person).where(Person.verified == True)
        verified_res = await session.execute(verified_stmt)
        verified_persons = verified_res.scalar_one()

        pending_stmt = select(func.count()).select_from(Registration).where(Registration.status == "pending")
        pending_res = await session.execute(pending_stmt)
        pending_count = pending_res.scalar_one()

        # recent cases
        recent_stmt = select(Person).order_by(Person.created_at.desc()).limit(5)
        recent_res = await session.execute(recent_stmt)
        recent = recent_res.scalars().all()
        recent_list = []
        for p in recent:
            recent_list.append({
                "person_id": str(p.id),
                "name": p.name,
                "case_id": p.case_id,
                "image_url": p.image_url,
                "created_at": p.created_at.isoformat() if p.created_at else None
            })

        return {
            "total_persons": int(total_persons),
            "verified_persons": int(verified_persons),
            "pending_registrations": int(pending_count),
            "recent_cases": recent_list
        }
