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
from ..cache.dashboard_cache import clear_dashboard_cache
from ..cache.person_cache import cache_person_metadata, invalidate_person_metadata

router = APIRouter()

@router.get("/admin/registrations")
async def admin_registrations(_=Depends(verify_clerk_admin_token)):
    async with AsyncSessionLocal() as session:
        stmt = select(Registration).where(Registration.status == "pending")
        res = await session.execute(stmt)
        regs = res.scalars().all()

        out = []
        for r in regs:
            out.append({
                "registration_id": str(r.id),
                "person_data": json.loads(r.person_data),
                "person_image_url": r.person_image_url,
                "aadhar_image_url": r.aadhar_image_url,
                "submitted_at": r.submitted_at.isoformat(),
            })
        return {"pending": out}


@router.post("/admin/verify/{registration_id}")
async def admin_verify(registration_id: str, approve: bool = True, _=Depends(verify_clerk_admin_token)):

    async with AsyncSessionLocal() as session:
        stmt = select(Registration).where(Registration.id == registration_id)
        reg = (await session.execute(stmt)).scalar_one_or_none()

        if not reg:
            raise HTTPException(status_code=404, detail="Registration not found")

        if not approve:
            await session.delete(reg)
            await session.commit()
            invalidate_person_metadata()
            return {"status": "rejected"}

        pdata = json.loads(reg.person_data)

        # Download face image
        try:
            resp = requests.get(reg.person_image_url)
            arr = np.frombuffer(resp.content, np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        except:
            raise HTTPException(500, "Failed to download face image")

        embedding = extract_embedding(img)

        new_id = uuid.uuid4()
        case_id = await generate_next_case_id()

        person = Person(
            id=new_id,
            name=pdata["name"],
            age=pdata["age"],
            gender=pdata["gender"],
            last_seen_location=pdata["last_seen_location"],
            last_seen_date=pdata["last_seen_date"],
            last_seen_time=pdata["last_seen_time"],
            contact_info=pdata["contact_info"],
            additional_details=pdata["additional_details"],
            height=pdata.get("height"),
            reported_by=pdata.get("reporter"),
            reporter_contact=pdata.get("reporter_contact"),
            image_url=reg.person_image_url,
            case_id=case_id,
            case_status="active",
            verified=True,
            created_at=datetime.utcnow(),
        )

        session.add(person)
        await session.commit()

        # Cache metadata
        cache_person_metadata(str(person.id), {
            "person_id": str(person.id),
            "name": person.name,
            "age": person.age,
            "image_url": person.image_url,
            "case_id": person.case_id,
            "last_seen_location": person.last_seen_location,
        })

        # Upsert embedding into Qdrant
        if embedding is not None:
            upsert_point(str(person.id), embedding, {
                "person_id": str(person.id),
                "verified": True,
                "image_url": person.image_url,
            })

        # Delete registration + clear dashboard
        await session.delete(reg)
        await session.commit()
        clear_dashboard_cache()

        return {"status": "approved", "person_id": str(person.id)}


@router.get("/admin/dashboard")
async def admin_dashboard(_=Depends(verify_clerk_admin_token)):
    from ..cache.dashboard_cache import get_dashboard_cache, set_dashboard_cache

    cached = get_dashboard_cache()
    if cached:
        return cached

    async with AsyncSessionLocal() as session:
        total = (await session.execute(select(func.count()).select_from(Person))).scalar()
        verified = (await session.execute(
            select(func.count()).select_from(Person).where(Person.verified == True)
        )).scalar()
        pending = (await session.execute(
            select(func.count()).select_from(Registration).where(Registration.status == "pending")
        )).scalar()

        # Fetch recent 5
        stmt = select(Person).order_by(Person.created_at.desc()).limit(5)
        res = await session.execute(stmt)
        recent = res.scalars().all()

        recent_list = [{
            "person_id": str(p.id),
            "name": p.name,
            "case_id": p.case_id,
            "image_url": p.image_url,
            "created_at": p.created_at.isoformat(),
        } for p in recent]

        dashboard = {
            "total_persons": total,
            "verified_persons": verified,
            "pending_registrations": pending,
            "recent_cases": recent_list,
        }

        set_dashboard_cache(dashboard)
        return dashboard
    
@router.get("/admin/approved")
async def admin_approved(_=Depends(verify_clerk_admin_token)):
    async with AsyncSessionLocal() as session:
        stmt = select(Person).where(Person.verified == True)
        res = await session.execute(stmt)
        persons = res.scalars().all()

        return [{
            "person_id": str(p.id),
            "name": p.name,
            "case_id": p.case_id,
            "image_url": p.image_url,
            "created_at": p.created_at.isoformat()
        } for p in persons]


@router.get("/admin/rejected")
async def admin_rejected(_=Depends(verify_clerk_admin_token)):
    async with AsyncSessionLocal() as session:
        stmt = select(Registration).where(Registration.status == "rejected")
        res = await session.execute(stmt)
        items = res.scalars().all()

        out = []
        for r in items:
            out.append({
                "registration_id": str(r.id),
                "person_data": json.loads(r.person_data),
                "submitted_at": r.submitted_at.isoformat(),
            })
        return {"rejected": out}