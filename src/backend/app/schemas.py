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
