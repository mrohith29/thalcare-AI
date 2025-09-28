from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    user_type: str
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None

class PatientCreate(ProfileBase):
    age: int
    gender: str
    blood_type: str

class DonorCreate(ProfileBase):
    age: int
    gender: str
    blood_type: str

class HospitalCreate(ProfileBase):
    hospital_name: str
    services: Optional[List[str]] = []
