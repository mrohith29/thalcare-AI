from sqlalchemy import Column, String, Integer, Boolean, Date, ForeignKey, Text, ARRAY, DECIMAL, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())


class Profile(Base):
    __tablename__ = "profiles"  
    id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    user_type = Column(String, nullable=False)  # patient, donor, doctor, hospital
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String)
    address = Column(Text)
    city = Column(String)
    state = Column(String)
    country = Column(String, default="India")
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())


class Patient(Base):
    __tablename__ = "patients"
    id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True)
    age = Column(Integer)
    gender = Column(String)
    blood_type = Column(String)
    thalassemia_type = Column(String)
    severity_level = Column(String)
    diagnosis_date = Column(Date)
    current_requirements = Column(Text)
    emergency_contact_name = Column(String)
    emergency_contact_phone = Column(String)
    insurance_provider = Column(String)


class Donor(Base):
    __tablename__ = "donors"
    id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True)
    age = Column(Integer)
    gender = Column(String)
    blood_type = Column(String)
    last_donation_date = Column(Date)
    total_donations = Column(Integer, default=0)
    available = Column(Boolean, default=True)
    contact_preference = Column(String, default="email")
    emergency_contact = Column(Boolean, default=False)
    health_conditions = Column(ARRAY(Text))


class Hospital(Base):
    __tablename__ = "hospitals"
    id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True)
    hospital_name = Column(String, nullable=False)
    services = Column(ARRAY(Text), default=[])
    thalassemia_specialist = Column(Boolean, default=False)
    rating = Column(DECIMAL(3, 2), default=0.00)
    total_ratings = Column(Integer, default=0)
    emergency_contact = Column(String)
    website = Column(String)
    insurance_accepted = Column(ARRAY(Text))
