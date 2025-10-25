from utils.supabase_client import get_Supabase
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid
from datetime import datetime

app = FastAPI()

class LoginRequest(BaseModel):
    email: str
    password: str
    model_config = {"extra": "ignore"}

class SignupRequest(BaseModel):
    # Auth
    email: str
    password: str

    # Common profile fields
    user_type: str  # 'patient' | 'donor' | 'doctor' | 'hospital'
    name: Optional[str] = None  # fallback display name; for hospital -> hospital_name
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None

    # Patient extras (optional)
    blood_type: Optional[str] = None
    thalassemia_type: Optional[str] = None
    severity_level: Optional[str] = None

    # Donor extras (optional)
    last_donation: Optional[str] = Field(default=None, description="ISO date for last donation")
    contact_preference: Optional[str] = None  # 'email' | 'phone' | 'both'

    # Hospital extras (optional)
    services: Optional[str] = None  # comma separated string from UI
    thalassemia_specialist: Optional[bool] = False
    model_config = {"extra": "ignore"}

class ProfileUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    model_config = {"extra": "ignore"}

class SearchRequest(BaseModel):
    user_type: Optional[str] = None
    blood_type: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    thalassemia_specialist: Optional[bool] = None
    available: Optional[bool] = None
    model_config = {"extra": "ignore"}

@app.post("/login")
def login(request: LoginRequest):
    supabase = get_Supabase()
    
    try:
        result = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        
        # Get user profile
        profile = supabase.table('profiles').select('*').eq('id', result.user.id).single().execute()
        
        return {
            "message": "Login successful",
            "access_token": result.session.access_token,
            "user_id": result.user.id,
            "profile": profile.data
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/signup")
def signup(request: SignupRequest):
    supabase = get_Supabase()
    
    try:
        # Sign up with Supabase Auth
        result = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password
        })
        
        if result.user:
            # Create profile in profiles table
            profile_data = {
                "id": result.user.id,
                "user_type": request.user_type,
                "first_name": request.first_name or "",
                "last_name": request.last_name or "",
                "email": request.email,
                "phone": request.phone,
                "address": request.address,
                "city": request.city,
                "state": request.state
            }
            
            supabase.table('profiles').insert(profile_data).execute()
            
            # Create specific profile based on user type
            if request.user_type == "patient":
                patient_data = {
                    "id": result.user.id,
                    "blood_type": request.blood_type,
                    "thalassemia_type": request.thalassemia_type,
                    "severity_level": request.severity_level
                }
                supabase.table('patients').insert(patient_data).execute()
                
            elif request.user_type == "donor":
                donor_data = {
                    "id": result.user.id,
                    "blood_type": request.blood_type,
                    "last_donation_date": request.last_donation,
                    "contact_preference": request.contact_preference or "email"
                }
                supabase.table('donors').insert(donor_data).execute()
                
            elif request.user_type == "hospital":
                hospital_data = {
                    "id": result.user.id,
                    "hospital_name": request.name,
                    "services": request.services.split(',') if request.services else [],
                    "thalassemia_specialist": request.thalassemia_specialist or False
                }
                supabase.table('hospitals').insert(hospital_data).execute()
                
            elif request.user_type == "doctor":
                doctor_data = {
                    "id": result.user.id,
                    "specialization": "General Medicine",  # Default, can be updated later
                    "thalassemia_specialist": False  # Default, can be updated later
                }
                supabase.table('doctors').insert(doctor_data).execute()
        
        return {"message": "Verification email sent. Please check your inbox to verify your email."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/profiles")
def get_profiles(user_type: Optional[str] = None, limit: int = 50, offset: int = 0):
    supabase = get_Supabase()
    
    try:
        query = supabase.table('profiles').select('*').eq('is_active', True)
        
        if user_type:
            query = query.eq('user_type', user_type)
            
        result = query.range(offset, offset + limit - 1).execute()
        return {"profiles": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profiles/{profile_id}")
def get_profile(profile_id: str):
    supabase = get_Supabase()
    
    try:
        # Get basic profile
        profile = supabase.table('profiles').select('*').eq('id', profile_id).single().execute()
        
        if not profile.data:
            raise HTTPException(status_code=404, detail="Profile not found")
            
        # Get specific profile data based on user type
        user_type = profile.data['user_type']
        specific_data = {}
        
        if user_type == "patient":
            patient = supabase.table('patients').select('*').eq('id', profile_id).single().execute()
            specific_data = patient.data or {}
        elif user_type == "donor":
            donor = supabase.table('donors').select('*').eq('id', profile_id).single().execute()
            specific_data = donor.data or {}
        elif user_type == "doctor":
            doctor = supabase.table('doctors').select('*').eq('id', profile_id).single().execute()
            specific_data = doctor.data or {}
        elif user_type == "hospital":
            hospital = supabase.table('hospitals').select('*').eq('id', profile_id).single().execute()
            specific_data = hospital.data or {}
            
        return {
            "profile": profile.data,
            "specific_data": specific_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/profiles/{profile_id}")
def update_profile(profile_id: str, request: ProfileUpdateRequest):
    supabase = get_Supabase()
    
    try:
        # Update basic profile
        update_data = {k: v for k, v in request.dict().items() if v is not None}
        if update_data:
            supabase.table('profiles').update(update_data).eq('id', profile_id).execute()
            
        return {"message": "Profile updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
def search_profiles(request: SearchRequest):
    supabase = get_Supabase()
    
    try:
        # Start with profiles table
        query = supabase.table('profiles').select('*').eq('is_active', True)
        
        if request.user_type:
            query = query.eq('user_type', request.user_type)
        if request.city:
            query = query.ilike('city', f'%{request.city}%')
        if request.state:
            query = query.ilike('state', f'%{request.state}%')
            
        profiles = query.execute()
        
        # Filter by specific criteria
        filtered_profiles = []
        for profile in profiles.data:
            include_profile = True
            
            # Check blood type for patients and donors
            if request.blood_type and profile['user_type'] in ['patient', 'donor']:
                specific_table = 'patients' if profile['user_type'] == 'patient' else 'donors'
                specific_data = supabase.table(specific_table).select('blood_type').eq('id', profile['id']).single().execute()
                if specific_data.data and specific_data.data['blood_type'] != request.blood_type:
                    include_profile = False
                    
            # Check thalassemia specialist for doctors and hospitals
            if request.thalassemia_specialist is not None and profile['user_type'] in ['doctor', 'hospital']:
                specific_table = 'doctors' if profile['user_type'] == 'doctor' else 'hospitals'
                specific_data = supabase.table(specific_table).select('thalassemia_specialist').eq('id', profile['id']).single().execute()
                if specific_data.data and specific_data.data['thalassemia_specialist'] != request.thalassemia_specialist:
                    include_profile = False
                    
            # Check availability for donors and doctors
            if request.available is not None and profile['user_type'] in ['donor', 'doctor']:
                specific_table = 'donors' if profile['user_type'] == 'donor' else 'doctors'
                specific_data = supabase.table(specific_table).select('available').eq('id', profile['id']).single().execute()
                if specific_data.data and specific_data.data['available'] != request.available:
                    include_profile = False
                    
            if include_profile:
                filtered_profiles.append(profile)
                
        return {"profiles": filtered_profiles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def get_stats():
    supabase = get_Supabase()
    
    try:
        # Get counts for each user type
        stats = {}
        user_types = ['patient', 'donor', 'doctor', 'hospital']
        
        for user_type in user_types:
            count = supabase.table('profiles').select('id', count='exact').eq('user_type', user_type).eq('is_active', True).execute()
            stats[f"{user_type}_count"] = count.count or 0
            
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

