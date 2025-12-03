# src/backend/app/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class MatchItem(BaseModel):
    person_id: str
    similarity: float
    image_url: str
    name: Optional[str] = None
    age: Optional[int] = None
    last_seen_location: Optional[str] = None
    case_id: Optional[str] = None

class SearchResponse(BaseModel):
    matches: List[MatchItem]

class RegisterRequest(BaseModel):
    name: str
    age: int
    gender: str
    last_seen_location: str
    last_seen_date: str
    last_seen_time: str
    contact_info: str
    additional_details: str
    height: Optional[str] = None
    reporter: Optional[str] = None
    reporter_contact: Optional[str] = None
    aadhar_number: Optional[str] = None

# Registration response (after submit)
class RegistrationResponse(BaseModel):
    registration_id: str
    status: str

# Admin side registration item
class AdminRegistrationItem(BaseModel):
    registration_id: str
    person_data: dict
    person_image_url: Optional[str] = None
    aadhar_image_url: Optional[str] = None
    submitted_at: Optional[str] = None

class AdminRegistrationList(BaseModel):
    pending: List[AdminRegistrationItem]

class ApproveRegistrationResponse(BaseModel):
    status: str
    person_id: Optional[str] = None

class AdminDashboardResponse(BaseModel):
    total_persons: int
    verified_persons: int
    pending_registrations: int
    recent_cases: List[dict]
