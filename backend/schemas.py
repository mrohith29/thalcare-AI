from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date

# Authentication schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str

# User creation
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Profile schemas
class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = "India"

class ProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

# Patient schemas
class PatientProfile(ProfileBase):
    age: Optional[int] = None
    gender: Optional[str] = None
    blood_type: Optional[str] = None
    thalassemia_type: Optional[str] = None
    severity_level: Optional[str] = None
    diagnosis_date: Optional[date] = None
    current_requirements: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    insurance_provider: Optional[str] = None

class PatientUpdate(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    blood_type: Optional[str] = None
    thalassemia_type: Optional[str] = None
    severity_level: Optional[str] = None
    diagnosis_date: Optional[date] = None
    current_requirements: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    insurance_provider: Optional[str] = None

# Donor schemas
class DonorProfile(ProfileBase):
    age: Optional[int] = None
    gender: Optional[str] = None
    blood_type: Optional[str] = None
    last_donation_date: Optional[date] = None
    total_donations: Optional[int] = 0
    available: Optional[bool] = True
    contact_preference: Optional[str] = "email"
    emergency_contact: Optional[bool] = False
    health_conditions: Optional[List[str]] = []

class DonorUpdate(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    blood_type: Optional[str] = None
    last_donation_date: Optional[date] = None
    available: Optional[bool] = None
    contact_preference: Optional[str] = None
    emergency_contact: Optional[bool] = None
    health_conditions: Optional[List[str]] = None

# Hospital schemas
class HospitalProfile(ProfileBase):
    hospital_name: str
    services: Optional[List[str]] = []
    thalassemia_specialist: Optional[bool] = False
    rating: Optional[float] = 0.0
    total_ratings: Optional[int] = 0
    emergency_contact: Optional[str] = None
    website: Optional[str] = None
    insurance_accepted: Optional[List[str]] = []

class HospitalUpdate(BaseModel):
    hospital_name: Optional[str] = None
    services: Optional[List[str]] = None
    thalassemia_specialist: Optional[bool] = None
    emergency_contact: Optional[str] = None
    website: Optional[str] = None
    insurance_accepted: Optional[List[str]] = None

# Full registration schemas combining all
class PatientRegistration(PatientProfile, UserCreate):
    pass

class DonorRegistration(DonorProfile, UserCreate):
    pass

class HospitalRegistration(HospitalProfile, UserCreate):
    pass

# Response schemas
class ProfileResponse(BaseModel):
    id: str
    email: str
    user_type: str
    first_name: str
    last_name: str
    phone: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: str
    is_active: bool
    created_at: str

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: str
    email: str
    created_at: str

    class Config:
        from_attributes = True

# Search schemas
class SearchRequest(BaseModel):
    user_type: Optional[str] = None
    blood_type: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    thalassemia_specialist: Optional[bool] = None
    available: Optional[bool] = None
    limit: int = 50
    offset: int = 0
