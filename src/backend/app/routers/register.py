# src/backend/app/routers/register.py
import uuid
import json
import requests
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from ..services.cloudinary_services import upload_image_fileobj
from ..services.db_service import AsyncSessionLocal
from src.backend.db_files.models import Registration
from ..pipeline import extract_embedding
from ..schemas import RegisterRequest, RegistrationResponse
from datetime import datetime

router = APIRouter()

@router.post("/register", response_model=RegistrationResponse)
async def register_person(
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    last_seen_location: str = Form(...),
    last_seen_date: str = Form(...),
    last_seen_time: str = Form(...),
    contact_info: str = Form(...),
    additional_details: str = Form(...),
    height: str = Form(None),
    reporter: str = Form(None),
    reporter_contact: str = Form(None),
    aadhar_number: str = Form(None),
    image: UploadFile = File(...),
    aadhar_image: UploadFile = File(None),
):
    # Validate minimal fields (Pydantic is used on client side; server double-checks)
    if not image:
        raise HTTPException(status_code=400, detail="Face image is required")

    # Upload images to Cloudinary
    try:
        face_url = upload_image_fileobj(image.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cloudinary upload failed: {e}")

    aadhar_url = None
    if aadhar_image:
        try:
            aadhar_url = upload_image_fileobj(aadhar_image.file)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Aadhar upload failed: {e}")

    # compute embedding (use pipeline)
    # we need bytes -> np image; extract_embedding expects BGR numpy
    import numpy as np
    import cv2
    image.file.seek(0)
    b = image.file.read()
    nparr = np.frombuffer(b, np.uint8)
    img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    embedding = extract_embedding(img_bgr)
    # embedding may be None if detect failed
    if embedding is None:
        # still store registration, admin can manually verify image
        embedding_flag = False
    else:
        embedding_flag = True

    # create registration DB entry
    async with AsyncSessionLocal() as session:
        reg = Registration(
            person_data=json.dumps({
                "name": name,
                "age": age,
                "gender": gender,
                "last_seen_location": last_seen_location,
                "last_seen_date": last_seen_date,
                "last_seen_time": last_seen_time,
                "contact_info": contact_info,
                "additional_details": additional_details,
                "height": height,
                "reporter": reporter,
                "reporter_contact": reporter_contact,
                "aadhar_number": aadhar_number,
                "face_embedding_available": embedding_flag
            }),
            person_image_url=face_url,
            aadhar_image_url=aadhar_url,
            status="pending",
            submitted_at=datetime.utcnow()
        )
        session.add(reg)
        await session.commit()
        await session.refresh(reg)
        return {"registration_id": str(reg.id), "status": reg.status}
