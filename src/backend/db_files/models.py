import uuid 
from datetime import datetime 
from sqlalchemy import (
    Column, String, Integer, Date, Time , Text, Boolean, DateTime, Enum, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY ,FLOAT
from sqlalchemy.ext.declarative import declarative_base 

Base = declarative_base() # To create a ORM Model (Object Relational Mapper)

from sqlalchemy import types 
class Vector(types.UserDefinedType): #store ML embeddings (like sentence embeddings, image feature vectors) directly in PostgreSQL.
    def get_col_spec(self):
        return "VECTOR"
    # store ML embeddings (like sentence embeddings, image feature vectors) directly in PostgreSQL.
class Person(Base):
    __tablename__ = "persons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    last_seen_location = Column(String(255))
    last_seen_date = Column(Date)
    last_seen_time = Column(Time)
    contact_info = Column(String(50))
    height = Column(String(10))
    additional_details = Column(Text)
    case_id = Column(String(50), unique=True, nullable=False)
    case_status = Column(String(20), nullable=False)
    reported_by = Column(String(50))
    reporter_contact = Column(String(50))
    image_url = Column(String(255), nullable=False)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    qdrant_id = Column(String(255))
    
class Registration(Base):
    __tablename__ = "registrations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_data = Column(Text, nullable=False)  # store as JSON string
    person_image_url = Column(String(255))
    aadhar_image_url = Column(String(255))
    status = Column(String(20), default="pending")  # 'pending', 'approved', 'rejected'
    submitted_at = Column(DateTime, default=datetime.utcnow)
    reviewed_by = Column(String(100))
    reviewed_at = Column(DateTime)
    
class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)