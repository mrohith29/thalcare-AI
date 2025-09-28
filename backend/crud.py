# crud.py
from sqlalchemy.orm import Session
from models import User, Profile, Patient, Donor, Hospital
from schemas import UserCreate, PatientCreate, DonorCreate, HospitalCreate
import hashlib

def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(db: Session, user: UserCreate, profile_data, role: str):
    """
    Create a user with a related profile and role-specific table entry.
    
    Args:
        db: SQLAlchemy Session
        user: UserCreate Pydantic schema
        profile_data: PatientCreate, DonorCreate, or HospitalCreate
        role: str - 'patient', 'donor', or 'hospital'
    
    Returns:
        db_user: the created User instance
    """

    # 1️⃣ Create user
    db_user = User(email=user.email, password_hash=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # 2️⃣ Prepare profile data safely (avoid multiple user_type)
    profile_dict = profile_data.dict()
    profile_dict.pop("user_type", None)  # remove if present
    db_profile = Profile(id=db_user.id, user_type=role, **profile_dict)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    # 3️⃣ Create role-specific table entry
    if role == "patient":
        db_patient = Patient(
            id=db_profile.id,
            age=profile_data.age,
            gender=profile_data.gender,
            blood_type=profile_data.blood_type
        )
        db.add(db_patient)

    elif role == "donor":
        db_donor = Donor(
            id=db_profile.id,
            age=profile_data.age,
            gender=profile_data.gender,
            blood_type=profile_data.blood_type
        )
        db.add(db_donor)

    elif role == "hospital":
        db_hospital = Hospital(
            id=db_profile.id,
            hospital_name=profile_data.hospital_name,
            services=profile_data.services
        )
        db.add(db_hospital)

    else:
        raise ValueError(f"Invalid role: {role}")

    db.commit()
    return db_user
