# src/backend/app/routers/register.py
import uuid
import json
import requests
import numpy as np
import cv2
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from ..services.cloudinary_services import upload_image_fileobj
from ..services.db_service import AsyncSessionLocal
from src.backend.db_files.models import Registration
from ..pipeline import extract_embedding
from ..schemas import RegisterRequest, RegistrationResponse
from datetime import datetime
from ..schemas import RegistrationResponse
from ..cache.dashboard_cache import clear_dashboard_cache
from ..cache.embedding_cache import set_cached_embedding
from ..cache.search_cache import set_cached_search

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
    if not image:
        raise HTTPException(status_code=400, detail="Face image is required")

    # Upload images to Cloudinary
    try:
        face_url = upload_image_fileobj(image.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload face image: {e}")

    aadhar_url = None
    if aadhar_image:
        try:
            aadhar_url = upload_image_fileobj(aadhar_image.file)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload Aadhar image: {e}")

    # Extract embedding from face (cache-worthy)
    image.file.seek(0)
    img_bytes = await image.read()
    arr = np.frombuffer(img_bytes, np.uint8)
    img_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    embedding = extract_embedding(img_bgr)
    embedding_flag = embedding is not None

    if embedding_flag:
        set_cached_embedding(img_bytes, embedding)

    # Create registration entry
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
            submitted_at=datetime.utcnow(),
        )
        session.add(reg)
        await session.commit()
        await session.refresh(reg)

    # Invalidate admin dashboard (new pending registration)
    clear_dashboard_cache()

    return {"registration_id": str(reg.id), "status": reg.status}