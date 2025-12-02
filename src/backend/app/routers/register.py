from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from ..services.cloudinary_services import upload_image_fileobj
from src.backend.db_files.models import Registration
from ..services.db_service import AsyncSessionLocal
from datetime import datetime
import json
from ..pipeline import extract_embedding

router = APIRouter()

@router.post("/register")
async def register_person(
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    last_seen_location: str = Form(...),
    last_seen_date: str = Form(...),
    last_seen_time: str = Form(...),
    contact_info: str = Form(...),
    additional_details: str = Form(...),
    image: UploadFile = File(...),
):
    # upload image to cloudinary
    url = upload_image_fileobj(image.file)
    # prepare metadata
    person_data = {
        "name": name,
        "age": age,
        "gender": gender,
        "last_seen_location": last_seen_location,
        "last_seen_date": last_seen_date,
        "last_seen_time": last_seen_time,
        "contact_info": contact_info,
        "additional_details": additional_details,
        "created_at": datetime.utcnow().isoformat()
    }
    async with AsyncSessionLocal() as session:
        reg = Registration(person_data=json.dumps(person_data), person_image_url=url, status="pending")
        session.add(reg)
        await session.commit()
        await session.refresh(reg)
        return {"registration_id": str(reg.id), "status": "pending"}
