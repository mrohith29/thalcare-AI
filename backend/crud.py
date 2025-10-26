# crud.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models import User, Profile, Patient, Donor, Hospital
import hashlib
import uuid
from schemas import (
    UserCreate, PatientProfile, DonorProfile, HospitalProfile,
    ProfileUpdate, PatientUpdate, DonorUpdate, HospitalUpdate
)

def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(plain_password) == hashed_password

# User operations
def get_user_by_email(db: Session, email: str) -> User:
    """Get a user by email."""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: str) -> User:
    """Get a user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, email: str, password: str) -> User:
    """Create a new user."""
    hashed_password = hash_password(password)
    db_user = User(email=email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Profile operations
def get_profile(db: Session, user_id: str) -> Profile:
    """Get a profile by user ID."""
    # Convert string UUID to UUID object for query
    if isinstance(user_id, str):
        try:
            user_id = uuid.UUID(user_id)
        except ValueError:
            return None
    return db.query(Profile).filter(Profile.id == user_id).first()

def create_profile(db: Session, user_id: str, user_type: str, profile_data: dict) -> Profile:
    """Create a profile for a user."""
    db_profile = Profile(id=user_id, user_type=user_type, **profile_data)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_profile(db: Session, user_id: str, profile_data: ProfileUpdate) -> Profile:
    """Update a profile."""
    db_profile = get_profile(db, user_id)
    if not db_profile:
        return None
    
    update_data = profile_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_profile, key, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

# Patient operations
def create_patient_profile(db: Session, user_id: str, patient_data: PatientProfile) -> Patient:
    """Create a patient profile."""
    patient_dict = patient_data.dict(exclude={'first_name', 'last_name', 'phone', 'address', 'city', 'state', 'country'})
    db_patient = Patient(id=user_id, **patient_dict)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient(db: Session, user_id: str) -> Patient:
    """Get a patient by user ID."""
    # Convert string UUID to UUID object for query
    if isinstance(user_id, str):
        try:
            user_id = uuid.UUID(user_id)
        except ValueError:
            return None
    return db.query(Patient).filter(Patient.id == user_id).first()

def update_patient(db: Session, user_id: str, patient_data: PatientUpdate) -> Patient:
    """Update patient information."""
    db_patient = get_patient(db, user_id)
    if not db_patient:
        return None
    
    update_data = patient_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_patient, key, value)
    
    db.commit()
    db.refresh(db_patient)
    return db_patient

# Donor operations
def create_donor_profile(db: Session, user_id: str, donor_data: DonorProfile) -> Donor:
    """Create a donor profile."""
    donor_dict = donor_data.dict(exclude={'first_name', 'last_name', 'phone', 'address', 'city', 'state', 'country'})
    db_donor = Donor(id=user_id, **donor_dict)
    db.add(db_donor)
    db.commit()
    db.refresh(db_donor)
    return db_donor

def get_donor(db: Session, user_id: str) -> Donor:
    """Get a donor by user ID."""
    # Convert string UUID to UUID object for query
    if isinstance(user_id, str):
        try:
            user_id = uuid.UUID(user_id)
        except ValueError:
            return None
    return db.query(Donor).filter(Donor.id == user_id).first()

def update_donor(db: Session, user_id: str, donor_data: DonorUpdate) -> Donor:
    """Update donor information."""
    db_donor = get_donor(db, user_id)
    if not db_donor:
        return None
    
    update_data = donor_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_donor, key, value)
    
    db.commit()
    db.refresh(db_donor)
    return db_donor

# Hospital operations
def create_hospital_profile(db: Session, user_id: str, hospital_data: HospitalProfile) -> Hospital:
    """Create a hospital profile."""
    hospital_dict = hospital_data.dict(exclude={'first_name', 'last_name', 'phone', 'address', 'city', 'state', 'country'})
    db_hospital = Hospital(id=user_id, **hospital_dict)
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital

def get_hospital(db: Session, user_id: str) -> Hospital:
    """Get a hospital by user ID."""
    # Convert string UUID to UUID object for query
    if isinstance(user_id, str):
        try:
            user_id = uuid.UUID(user_id)
        except ValueError:
            return None
    return db.query(Hospital).filter(Hospital.id == user_id).first()

def update_hospital(db: Session, user_id: str, hospital_data: HospitalUpdate) -> Hospital:
    """Update hospital information."""
    db_hospital = get_hospital(db, user_id)
    if not db_hospital:
        return None
    
    update_data = hospital_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_hospital, key, value)
    
    db.commit()
    db.refresh(db_hospital)
    return db_hospital

# Search operations
def search_profiles(
    db: Session,
    user_type: str = None,
    blood_type: str = None,
    city: str = None,
    state: str = None,
    thalassemia_specialist: bool = None,
    available: bool = None,
    limit: int = 50,
    offset: int = 0
):
    """Search for profiles based on criteria."""
    query = db.query(Profile).filter(Profile.is_active == True)
    
    if user_type:
        query = query.filter(Profile.user_type == user_type)
    if city:
        query = query.filter(Profile.city.ilike(f"%{city}%"))
    if state:
        query = query.filter(Profile.state.ilike(f"%{state}%"))
    
    profiles = query.offset(offset).limit(limit).all()
    
    # Filter by blood type for patients and donors
    if blood_type:
        filtered_profiles = []
        for profile in profiles:
            if profile.user_type == 'patient':
                patient = get_patient(db, profile.id)
                if patient and patient.blood_type == blood_type:
                    filtered_profiles.append(profile)
            elif profile.user_type == 'donor':
                donor = get_donor(db, profile.id)
                if donor and donor.blood_type == blood_type:
                    filtered_profiles.append(profile)
        profiles = filtered_profiles
    
    # Filter by thalassemia specialist for hospitals
    if thalassemia_specialist is not None:
        filtered_profiles = []
        for profile in profiles:
            if profile.user_type == 'hospital':
                hospital = get_hospital(db, profile.id)
                if hospital and hospital.thalassemia_specialist == thalassemia_specialist:
                    filtered_profiles.append(profile)
        profiles = filtered_profiles
    
    # Filter by availability for donors
    if available is not None:
        filtered_profiles = []
        for profile in profiles:
            if profile.user_type == 'donor':
                donor = get_donor(db, profile.id)
                if donor and donor.available == available:
                    filtered_profiles.append(profile)
        profiles = filtered_profiles
    
    return profiles

# Statistics
def get_stats(db: Session):
    """Get statistics for each user type."""
    stats = {}
    user_types = ['patient', 'donor', 'hospital']
    
    for user_type in user_types:
        count = db.query(Profile).filter(
            and_(Profile.user_type == user_type, Profile.is_active == True)
        ).count()
        stats[f"{user_type}_count"] = count
    
    return stats
