from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import (
    LoginRequest, PatientRegistration, DonorRegistration, HospitalRegistration,
    ProfileUpdate, PatientUpdate, DonorUpdate, HospitalUpdate,
    SearchRequest, ProfileResponse
)
import crud
import uuid
from typing import Optional

router = APIRouter()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== Authentication Endpoints ====================

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user and return user information.
    
    This endpoint validates user credentials and returns user ID, email, and user type.
    Works for all user types: patients, donors, and hospitals.
    
    **Input Parameters:**
    - `email` (str, required): User's email address. Must be a valid email format.
    - `password` (str, required): User's password. Will be hashed and verified.
    
    **Request Body Example:**
    ```json
    {
        "email": "patient@example.com",
        "password": "SecurePassword123"
    }
    ```
    
    **Response:**
    - `message` (str): Success message
    - `user_id` (str): UUID of the authenticated user
    - `email` (str): User's email address
    - `user_type` (str): Type of user - either "patient", "donor", or "hospital"
    
    **Response Example:**
    ```json
    {
        "message": "Login successful",
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "patient@example.com",
        "user_type": "patient"
    }
    ```
    
    **Error Responses:**
    - 401 Unauthorized: Invalid email or password
    """
    user = crud.get_user_by_email(db, request.email)
    
    if not user or not crud.verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    profile = crud.get_profile(db, str(user.id))
    
    return {
        "message": "Login successful",
        "user_id": str(user.id),
        "email": user.email,
        "user_type": profile.user_type if profile else None
    }

# ==================== Registration Endpoints ====================

@router.post("/register/patient")
def register_patient(patient_data: PatientRegistration, db: Session = Depends(get_db)):
    """
    Register a new patient user with complete profile and medical information.
    
    This endpoint creates a new patient account with all related data including:
    - User credentials (email and password)
    - Profile information (name, contact, address)
    - Patient-specific medical data (blood type, thalassemia type, severity, etc.)
    
    **Input Parameters:**
    
    *Authentication Fields:*
    - `email` (str, required): Patient's email address (must be unique)
    - `password` (str, required): Password for the account
    
    *Profile Fields:*
    - `first_name` (str, required): Patient's first name
    - `last_name` (str, required): Patient's last name
    - `phone` (str, optional): Contact phone number
    - `address` (str, optional): Street address
    - `city` (str, optional): City name
    - `state` (str, optional): State/province name
    - `country` (str, optional): Defaults to "India" if not provided
    
    *Patient Medical Fields:*
    - `age` (int, optional): Patient's age
    - `gender` (str, optional): Gender (e.g., "Male", "Female")
    - `blood_type` (str, optional): Blood group (e.g., "O+", "A-", "B+", "AB+", "O-", "A-", "B-", "AB-")
    - `thalassemia_type` (str, optional): Type of thalassemia (e.g., "Alpha", "Beta")
    - `severity_level` (str, optional): Severity (e.g., "Mild", "Moderate", "Severe")
    - `diagnosis_date` (date, optional): Date of diagnosis (YYYY-MM-DD format)
    - `current_requirements` (str, optional): Current treatment needs
    - `emergency_contact_name` (str, optional): Emergency contact's name
    - `emergency_contact_phone` (str, optional): Emergency contact's phone
    - `insurance_provider` (str, optional): Insurance company name
    
    **Request Body Example:**
    ```json
    {
        "email": "john.patient@example.com",
        "password": "SecurePass123",
        "first_name": "John",
        "last_name": "Doe",
        "phone": "9876543210",
        "address": "123 Medical Street",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "age": 25,
        "gender": "Male",
        "blood_type": "O+",
        "thalassemia_type": "Beta Thalassemia",
        "severity_level": "Moderate",
        "diagnosis_date": "2020-05-15",
        "current_requirements": "Regular blood transfusions every 3 weeks",
        "emergency_contact_name": "Jane Doe",
        "emergency_contact_phone": "9876543211",
        "insurance_provider": "HealthCare Insurance"
    }
    ```
    
    **Response:**
    - `message` (str): Success message
    - `user_id` (str): UUID of the newly created user
    - `email` (str): Registered email address
    
    **Response Example:**
    ```json
    {
        "message": "Patient registered successfully",
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "john.patient@example.com"
    }
    ```
    
    **Error Responses:**
    - 400 Bad Request: Email already registered
    """
    # Check if email already exists
    existing_user = crud.get_user_by_email(db, patient_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = crud.create_user(db, patient_data.email, patient_data.password)
    
    # Create profile
    profile_data = {
        "first_name": patient_data.first_name,
        "last_name": patient_data.last_name,
        "phone": patient_data.phone,
        "address": patient_data.address,
        "city": patient_data.city,
        "state": patient_data.state,
        "country": patient_data.country
    }
    profile = crud.create_profile(db, str(user.id), "patient", profile_data)
    
    # Create patient-specific data
    patient = crud.create_patient_profile(db, str(user.id), patient_data)
    
    return {
        "message": "Patient registered successfully",
        "user_id": str(user.id),
        "email": user.email
    }

@router.post("/register/donor")
def register_donor(donor_data: DonorRegistration, db: Session = Depends(get_db)):
    """
    Register a new donor user with complete profile and donation information.
    
    This endpoint creates a new donor account with all related data including:
    - User credentials (email and password)
    - Profile information (name, contact, address)
    - Donor-specific data (blood type, availability, donation history, etc.)
    
    **Input Parameters:**
    
    *Authentication Fields:*
    - `email` (str, required): Donor's email address (must be unique)
    - `password` (str, required): Password for the account
    
    *Profile Fields:*
    - `first_name` (str, required): Donor's first name
    - `last_name` (str, required): Donor's last name
    - `phone` (str, optional): Contact phone number
    - `address` (str, optional): Street address
    - `city` (str, optional): City name
    - `state` (str, optional): State/province name
    - `country` (str, optional): Defaults to "India" if not provided
    
    *Donor Specific Fields:*
    - `age` (int, optional): Donor's age
    - `gender` (str, optional): Gender (e.g., "Male", "Female")
    - `blood_type` (str, optional): Blood group (e.g., "O+", "A-", "B+", "AB+")
    - `last_donation_date` (date, optional): Date of last donation (YYYY-MM-DD format)
    - `total_donations` (int, optional): Total number of donations (defaults to 0)
    - `available` (bool, optional): Whether currently available for donation (defaults to True)
    - `contact_preference` (str, optional): How to contact ("email", "phone", "both", defaults to "email")
    - `emergency_contact` (bool, optional): Available for emergency donations (defaults to False)
    - `health_conditions` (list[str], optional): List of health conditions or medications
    
    **Request Body Example:**
    ```json
    {
        "email": "donor.jane@example.com",
        "password": "SecurePass456",
        "first_name": "Jane",
        "last_name": "Smith",
        "phone": "9876543220",
        "address": "456 Donor Avenue",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "age": 30,
        "gender": "Female",
        "blood_type": "O+",
        "last_donation_date": "2024-01-15",
        "total_donations": 8,
        "available": true,
        "contact_preference": "email",
        "emergency_contact": true,
        "health_conditions": []
    }
    ```
    
    **Response:**
    - `message` (str): Success message
    - `user_id` (str): UUID of the newly created user
    - `email` (str): Registered email address
    
    **Response Example:**
    ```json
    {
        "message": "Donor registered successfully",
        "user_id": "660e8400-e29b-41d4-a716-446655440000",
        "email": "donor.jane@example.com"
    }
    ```
    
    **Error Responses:**
    - 400 Bad Request: Email already registered
    """
    # Check if email already exists
    existing_user = crud.get_user_by_email(db, donor_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = crud.create_user(db, donor_data.email, donor_data.password)
    
    # Create profile
    profile_data = {
        "first_name": donor_data.first_name,
        "last_name": donor_data.last_name,
        "phone": donor_data.phone,
        "address": donor_data.address,
        "city": donor_data.city,
        "state": donor_data.state,
        "country": donor_data.country
    }
    profile = crud.create_profile(db, str(user.id), "donor", profile_data)
    
    # Create donor-specific data
    donor = crud.create_donor_profile(db, str(user.id), donor_data)
    
    return {
        "message": "Donor registered successfully",
        "user_id": str(user.id),
        "email": user.email
    }

@router.post("/register/hospital")
def register_hospital(hospital_data: HospitalRegistration, db: Session = Depends(get_db)):
    """
    Register a new hospital user with complete profile and hospital information.
    
    This endpoint creates a new hospital account with all related data including:
    - User credentials (email and password)
    - Profile information (administrative contact, address)
    - Hospital-specific data (services, specialties, ratings, etc.)
    
    **Input Parameters:**
    
    *Authentication Fields:*
    - `email` (str, required): Hospital's email address (must be unique)
    - `password` (str, required): Password for the account
    
    *Profile Fields:*
    - `first_name` (str, required): Admin/contact person's first name
    - `last_name` (str, required): Admin/contact person's last name
    - `phone` (str, optional): Contact phone number
    - `address` (str, optional): Hospital address
    - `city` (str, optional): City name
    - `state` (str, optional): State/province name
    - `country` (str, optional): Defaults to "India" if not provided
    
    *Hospital Specific Fields:*
    - `hospital_name` (str, required): Official hospital name
    - `services` (list[str], optional): List of services offered (e.g., ["Emergency", "Surgery", "Blood Bank"])
    - `thalassemia_specialist` (bool, optional): Has thalassemia specialists (defaults to False)
    - `rating` (float, optional): Average rating (defaults to 0.0)
    - `total_ratings` (int, optional): Number of ratings received (defaults to 0)
    - `emergency_contact` (str, optional): Emergency contact number
    - `website` (str, optional): Hospital website URL
    - `insurance_accepted` (list[str], optional): List of accepted insurance providers
    
    **Request Body Example:**
    ```json
    {
        "email": "admin@cityhospital.com",
        "password": "SecurePass789",
        "first_name": "Dr. Rajesh",
        "last_name": "Kumar",
        "phone": "022-12345678",
        "address": "789 Healthcare Boulevard",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "hospital_name": "City Hospital",
        "services": ["Emergency", "Surgery", "Blood Bank", "Oncology", "Cardiology"],
        "thalassemia_specialist": true,
        "rating": 4.5,
        "total_ratings": 150,
        "emergency_contact": "022-98765432",
        "website": "https://cityhospital.com",
        "insurance_accepted": ["HealthCare Insurance", "Medicare", "InsurancePro"]
    }
    ```
    
    **Response:**
    - `message` (str): Success message
    - `user_id` (str): UUID of the newly created user
    - `email` (str): Registered email address
    
    **Response Example:**
    ```json
    {
        "message": "Hospital registered successfully",
        "user_id": "770e8400-e29b-41d4-a716-446655440000",
        "email": "admin@cityhospital.com"
    }
    ```
    
    **Error Responses:**
    - 400 Bad Request: Email already registered
    """
    # Check if email already exists
    existing_user = crud.get_user_by_email(db, hospital_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = crud.create_user(db, hospital_data.email, hospital_data.password)
    
    # Create profile
    profile_data = {
        "first_name": hospital_data.first_name,
        "last_name": hospital_data.last_name,
        "phone": hospital_data.phone,
        "address": hospital_data.address,
        "city": hospital_data.city,
        "state": hospital_data.state,
        "country": hospital_data.country
    }
    profile = crud.create_profile(db, str(user.id), "hospital", profile_data)
    
    # Create hospital-specific data
    hospital = crud.create_hospital_profile(db, str(user.id), hospital_data)
    
    return {
        "message": "Hospital registered successfully",
        "user_id": str(user.id),
        "email": user.email
    }

# ==================== Profile Management ====================

@router.get("/profile/{user_id}", response_model=ProfileResponse)
def get_profile(user_id: str, db: Session = Depends(get_db)):
    """
    Get a user's profile information.
    
    Retrieves the basic profile information for any user type (patient, donor, or hospital).
    
    **Path Parameters:**
    - `user_id` (str, required): UUID of the user. Must be a valid UUID format.
    
    **Response Fields:**
    - `id` (str): User's unique identifier (UUID)
    - `email` (str): User's email address
    - `user_type` (str): Type of user ("patient", "donor", or "hospital")
    - `first_name` (str): User's first name
    - `last_name` (str): User's last name
    - `phone` (str, nullable): Contact phone number
    - `address` (str, nullable): Street address
    - `city` (str, nullable): City name
    - `state` (str, nullable): State/province name
    - `country` (str): Country name (defaults to "India")
    - `is_active` (bool): Whether the account is active
    - `created_at` (str): Account creation timestamp (ISO format)
    
    **Response Example:**
    ```json
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "john.patient@example.com",
        "user_type": "patient",
        "first_name": "John",
        "last_name": "Doe",
        "phone": "9876543210",
        "address": "123 Medical Street",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "is_active": true,
        "created_at": "2024-01-15T10:30:00"
    }
    ```
    
    **Error Responses:**
    - 404 Not Found: Profile not found for the given user_id
    """
    profile = crud.get_profile(db, user_id)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return profile

@router.put("/profile/{user_id}")
def update_profile(user_id: str, profile_data: ProfileUpdate, db: Session = Depends(get_db)):
    """
    Update a user's profile information.
    
    Allows updating any profile field. Only provided fields will be updated.
    All fields are optional - send only the fields you want to update.
    
    **Path Parameters:**
    - `user_id` (str, required): UUID of the user to update
    
    **Request Body Fields (all optional):**
    - `first_name` (str, optional): New first name
    - `last_name` (str, optional): New last name
    - `phone` (str, optional): New phone number
    - `address` (str, optional): New address
    - `city` (str, optional): New city
    - `state` (str, optional): New state
    - `country` (str, optional): New country
    
    **Request Body Example:**
    ```json
    {
        "first_name": "Johnny",
        "phone": "9876543211",
        "city": "Delhi"
    }
    ```
    
    **Response:**
    - `message` (str): Success confirmation message
    
    **Response Example:**
    ```json
    {
        "message": "Profile updated successfully"
    }
    ```
    
    **Error Responses:**
    - 404 Not Found: Profile not found for the given user_id
    """
    profile = crud.update_profile(db, user_id, profile_data)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return {"message": "Profile updated successfully"}

# ==================== Patient-Specific Endpoints ====================

@router.get("/patient/{user_id}")
def get_patient_data(user_id: str, db: Session = Depends(get_db)):
    """
    Get patient-specific medical data.
    
    Retrieves detailed medical information for a patient including:
    blood type, thalassemia type, severity, diagnosis details, and treatment requirements.
    
    **Path Parameters:**
    - `user_id` (str, required): UUID of the patient. Must be a valid UUID.
    
    **Response Fields:**
    - `id` (str): Patient's user ID
    - `age` (int, nullable): Patient's age
    - `gender` (str, nullable): Patient's gender
    - `blood_type` (str, nullable): Blood group
    - `thalassemia_type` (str, nullable): Type of thalassemia
    - `severity_level` (str, nullable): Severity of condition
    - `diagnosis_date` (date, nullable): Date of diagnosis
    - `current_requirements` (str, nullable): Current treatment needs
    - `emergency_contact_name` (str, nullable): Emergency contact's name
    - `emergency_contact_phone` (str, nullable): Emergency contact's phone
    - `insurance_provider` (str, nullable): Insurance provider name
    
    **Response Example:**
    ```json
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "age": 25,
        "gender": "Male",
        "blood_type": "O+",
        "thalassemia_type": "Beta Thalassemia",
        "severity_level": "Moderate",
        "diagnosis_date": "2020-05-15",
        "current_requirements": "Regular blood transfusions every 3 weeks",
        "emergency_contact_name": "Jane Doe",
        "emergency_contact_phone": "9876543211",
        "insurance_provider": "HealthCare Insurance"
    }
    ```
    
    **Error Responses:**
    - 404 Not Found: Patient data not found for the given user_id
    """
    patient = crud.get_patient(db, user_id)
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient data not found"
        )
    
    return patient

@router.put("/patient/{user_id}")
def update_patient_data(user_id: str, patient_data: PatientUpdate, db: Session = Depends(get_db)):
    """
    Update patient-specific medical data.
    
    Updates medical information for a patient. Only provided fields will be updated.
    Useful for updating treatment needs, severity level, or diagnosis information.
    
    **Path Parameters:**
    - `user_id` (str, required): UUID of the patient to update
    
    **Request Body Fields (all optional):**
    - `age` (int, optional): Updated age
    - `gender` (str, optional): Updated gender
    - `blood_type` (str, optional): Updated blood type
    - `thalassemia_type` (str, optional): Updated thalassemia type
    - `severity_level` (str, optional): Updated severity level
    - `diagnosis_date` (date, optional): Updated diagnosis date (YYYY-MM-DD)
    - `current_requirements` (str, optional): Updated treatment requirements
    - `emergency_contact_name` (str, optional): Updated emergency contact name
    - `emergency_contact_phone` (str, optional): Updated emergency contact phone
    - `insurance_provider` (str, optional): Updated insurance provider
    
    **Request Body Example:**
    ```json
    {
        "severity_level": "Severe",
        "current_requirements": "Weekly blood transfusions, iron chelation therapy"
    }
    ```
    
    **Response:**
    - `message` (str): Success confirmation message
    
    **Response Example:**
    ```json
    {
        "message": "Patient data updated successfully"
    }
    ```
    
    **Error Responses:**
    - 404 Not Found: Patient data not found for the given user_id
    """
    patient = crud.update_patient(db, user_id, patient_data)
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient data not found"
        )
    
    return {"message": "Patient data updated successfully"}

# ==================== Donor-Specific Endpoints ====================

@router.get("/donor/{user_id}")
def get_donor_data(user_id: str, db: Session = Depends(get_db)):
    """
    Get donor-specific donation information.
    
    Retrieves detailed information about a donor including:
    blood type, availability status, donation history, and contact preferences.
    
    **Path Parameters:**
    - `user_id` (str, required): UUID of the donor. Must be a valid UUID.
    
    **Response Fields:**
    - `id` (str): Donor's user ID
    - `age` (int, nullable): Donor's age
    - `gender` (str, nullable): Donor's gender
    - `blood_type` (str, nullable): Blood group (e.g., "O+", "A-")
    - `last_donation_date` (date, nullable): Date of last donation
    - `total_donations` (int): Total number of donations
    - `available` (bool): Whether currently available for donation
    - `contact_preference` (str): Preferred contact method
    - `emergency_contact` (bool): Available for emergency donations
    - `health_conditions` (list[str]): List of health conditions or medications
    
    **Response Example:**
    ```json
    {
        "id": "660e8400-e29b-41d4-a716-446655440000",
        "age": 30,
        "gender": "Female",
        "blood_type": "O+",
        "last_donation_date": "2024-01-15",
        "total_donations": 8,
        "available": true,
        "contact_preference": "email",
        "emergency_contact": true,
        "health_conditions": []
    }
    ```
    
    **Error Responses:**
    - 404 Not Found: Donor data not found for the given user_id
    """
    donor = crud.get_donor(db, user_id)
    
    if not donor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donor data not found"
        )
    
    return donor

@router.put("/donor/{user_id}")
def update_donor_data(user_id: str, donor_data: DonorUpdate, db: Session = Depends(get_db)):
    """
    Update donor-specific information.
    
    Updates donor information including availability status, donation dates,
    and contact preferences. Useful for donors to update their availability.
    
    **Path Parameters:**
    - `user_id` (str, required): UUID of the donor to update
    
    **Request Body Fields (all optional):**
    - `age` (int, optional): Updated age
    - `gender` (str, optional): Updated gender
    - `blood_type` (str, optional): Updated blood type
    - `last_donation_date` (date, optional): Updated last donation date (YYYY-MM-DD)
    - `available` (bool, optional): Updated availability status
    - `contact_preference` (str, optional): Updated contact preference
    - `emergency_contact` (bool, optional): Updated emergency contact availability
    - `health_conditions` (list[str], optional): Updated health conditions
    
    **Request Body Example:**
    ```json
    {
        "available": false,
        "last_donation_date": "2024-10-20",
        "contact_preference": "phone"
    }
    ```
    
    **Response:**
    - `message` (str): Success confirmation message
    
    **Response Example:**
    ```json
    {
        "message": "Donor data updated successfully"
    }
    ```
    
    **Error Responses:**
    - 404 Not Found: Donor data not found for the given user_id
    """
    donor = crud.update_donor(db, user_id, donor_data)
    
    if not donor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donor data not found"
        )
    
    return {"message": "Donor data updated successfully"}

# ==================== Hospital-Specific Endpoints ====================

@router.get("/hospital/{user_id}")
def get_hospital_data(user_id: str, db: Session = Depends(get_db)):
    """
    Get hospital-specific information.
    
    Retrieves detailed information about a hospital including:
    services offered, specialties, ratings, and operational details.
    
    **Path Parameters:**
    - `user_id` (str, required): UUID of the hospital. Must be a valid UUID.
    
    **Response Fields:**
    - `id` (str): Hospital's user ID
    - `hospital_name` (str): Official hospital name
    - `services` (list[str]): List of services offered
    - `thalassemia_specialist` (bool): Has thalassemia specialists
    - `rating` (float): Average rating
    - `total_ratings` (int): Number of ratings received
    - `emergency_contact` (str, nullable): Emergency contact number
    - `website` (str, nullable): Hospital website URL
    - `insurance_accepted` (list[str]): List of accepted insurance providers
    
    **Response Example:**
    ```json
    {
        "id": "770e8400-e29b-41d4-a716-446655440000",
        "hospital_name": "City Hospital",
        "services": ["Emergency", "Surgery", "Blood Bank", "Oncology"],
        "thalassemia_specialist": true,
        "rating": 4.5,
        "total_ratings": 150,
        "emergency_contact": "022-98765432",
        "website": "https://cityhospital.com",
        "insurance_accepted": ["HealthCare Insurance", "Medicare"]
    }
    ```
    
    **Error Responses:**
    - 404 Not Found: Hospital data not found for the given user_id
    """
    hospital = crud.get_hospital(db, user_id)
    
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital data not found"
        )
    
    return hospital

@router.put("/hospital/{user_id}")
def update_hospital_data(user_id: str, hospital_data: HospitalUpdate, db: Session = Depends(get_db)):
    """
    Update hospital-specific information.
    
    Updates hospital information including services, specialties, and contact details.
    Useful for hospitals to update their services and ratings.
    
    **Path Parameters:**
    - `user_id` (str, required): UUID of the hospital to update
    
    **Request Body Fields (all optional):**
    - `hospital_name` (str, optional): Updated hospital name
    - `services` (list[str], optional): Updated list of services
    - `thalassemia_specialist` (bool, optional): Updated specialist status
    - `emergency_contact` (str, optional): Updated emergency contact
    - `website` (str, optional): Updated website URL
    - `insurance_accepted` (list[str], optional): Updated insurance providers
    
    **Request Body Example:**
    ```json
    {
        "services": ["Emergency", "Surgery", "Blood Bank", "Oncology", "Cardiology"],
        "thalassemia_specialist": true
    }
    ```
    
    **Response:**
    - `message` (str): Success confirmation message
    
    **Response Example:**
    ```json
    {
        "message": "Hospital data updated successfully"
    }
    ```
    
    **Error Responses:**
    - 404 Not Found: Hospital data not found for the given user_id
    """
    hospital = crud.update_hospital(db, user_id, hospital_data)
    
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital data not found"
        )
    
    return {"message": "Hospital data updated successfully"}

# ==================== Cross-Type Discovery Endpoints ====================

@router.get("/donors/available")
def get_available_donors(
    blood_type: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get list of available donors with comprehensive filters.
    
    Retrieves donors who are currently available for blood donation with optional filtering.
    Useful for patients or hospitals looking for blood donors with specific criteria.
    
    **Query Parameters:**
    - `blood_type` (str, optional): Filter by blood type (e.g., "O+", "A-", "B+", "AB+", "O-", "B-", "AB-")
    - `city` (str, optional): Filter by city name. Partial match supported.
    - `state` (str, optional): Filter by state/province name. Partial match supported.
    - `limit` (int, optional): Maximum number of results (default: 50, max recommended: 100)
    - `offset` (int, optional): Number of results to skip for pagination (default: 0)
    
    **Request Examples:**
    ```bash
    GET /api/donors/available?blood_type=O+&city=Mumbai&limit=20
    GET /api/donors/available?city=Delhi&state=Delhi
    GET /api/donors/available?blood_type=AB+&limit=10&offset=0
    ```
    
    **Response:**
    - `donors` (list): Array of donor objects, each containing:
      - `profile` (object): Donor's profile information (name, contact, location)
      - `donor_data` (object): Donor-specific data (blood type, availability, donation history)
    - `count` (int): Number of donors in the response
    
    **Response Example:**
    ```json
    {
        "donors": [
            {
                "profile": {
                    "id": "uuid",
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "city": "Mumbai",
                    "phone": "9876543220",
                    "user_type": "donor"
                },
                "donor_data": {
                    "blood_type": "O+",
                    "available": true,
                    "last_donation_date": "2024-01-15",
                    "total_donations": 8
                }
            }
        ],
        "count": 1
    }
    ```
    """
    profiles = crud.search_profiles(
        db,
        user_type="donor",
        blood_type=blood_type,
        city=city,
        state=state,
        available=True,
        limit=limit,
        offset=offset
    )
    
    # Enrich with donor-specific data
    donor_list = []
    for profile in profiles:
        donor = crud.get_donor(db, str(profile.id))
        if donor:
            donor_list.append({
                "profile": profile,
                "donor_data": donor
            })
    
    return {"donors": donor_list, "count": len(donor_list)}

@router.get("/donors/nearby")
def get_nearby_donors(
    city: str,
    blood_type: Optional[str] = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get nearby available donors by city.
    
    Quick access endpoint to find donors in a specific city. Optimized for mobile apps
    and quick searches. Returns only available donors.
    
    **Query Parameters:**
    - `city` (str, required): City name to search in. Partial match supported.
    - `blood_type` (str, optional): Filter by blood type (e.g., "O+", "A-")
    - `limit` (int, optional): Maximum number of results (default: 20)
    
    **Request Examples:**
    ```bash
    GET /api/donors/nearby?city=Mumbai&blood_type=A+
    GET /api/donors/nearby?city=Delhi&limit=50
    ```
    
    **Response:**
    Same structure as `/api/donors/available` endpoint
    
    **Use Case:** 
    Patient needs urgent blood in their city. Quick search for nearby donors.
    """
    return get_available_donors(blood_type=blood_type, city=city, limit=limit, db=db)

@router.get("/donors/blood-type/{blood_type}")
def get_donors_by_blood_type(
    blood_type: str,
    city: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get donors by specific blood type.
    
    Retrieves all available donors with a specific blood type. Essential for
    finding compatible blood donors for patients.
    
    **Path Parameters:**
    - `blood_type` (str, required): Blood type to search for (e.g., "O+", "A-", "B+", "AB+", "O-", "B-", "AB-")
    
    **Query Parameters:**
    - `city` (str, optional): Filter by city name for location-specific results
    - `limit` (int, optional): Maximum number of results (default: 50)
    
    **Request Examples:**
    ```bash
    GET /api/donors/blood-type/O+?city=Delhi
    GET /api/donors/blood-type/AB+?limit=100
    ```
    
    **Response:**
    Same structure as `/api/donors/available` endpoint
    
    **Use Case:**
    Patient needs O+ blood specifically. Search all O+ donors.
    """
    return get_available_donors(blood_type=blood_type, city=city, limit=limit, db=db)

@router.get("/hospitals/specialist")
def get_thalassemia_specialist_hospitals(
    city: Optional[str] = None,
    state: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get hospitals with thalassemia specialists.
    
    Retrieves hospitals that have thalassemia specialists. Critical for patients
    who need specialized care for their condition.
    
    **Query Parameters:**
    - `city` (str, optional): Filter by city name
    - `state` (str, optional): Filter by state/province name
    - `limit` (int, optional): Maximum number of results (default: 50)
    - `offset` (int, optional): Pagination offset (default: 0)
    
    **Request Examples:**
    ```bash
    GET /api/hospitals/specialist?city=Mumbai&state=Maharashtra
    GET /api/hospitals/specialist?state=Karnataka&limit=30
    ```
    
    **Response:**
    - `hospitals` (list): Array of hospital objects with profile and hospital_data
    - `count` (int): Number of hospitals found
    
    **Response Example:**
    ```json
    {
        "hospitals": [
            {
                "profile": {
                    "id": "uuid",
                    "first_name": "Admin",
                    "city": "Mumbai",
                    "phone": "1234567890"
                },
                "hospital_data": {
                    "hospital_name": "City Hospital",
                    "thalassemia_specialist": true,
                    "services": ["Emergency", "Surgery", "Blood Bank"],
                    "rating": 4.5
                }
            }
        ],
        "count": 1
    }
    ```
    """
    profiles = crud.search_profiles(
        db,
        user_type="hospital",
        city=city,
        state=state,
        thalassemia_specialist=True,
        limit=limit,
        offset=offset
    )
    
    # Enrich with hospital-specific data
    hospital_list = []
    for profile in profiles:
        hospital = crud.get_hospital(db, str(profile.id))
        if hospital and hospital.thalassemia_specialist:
            hospital_list.append({
                "profile": profile,
                "hospital_data": hospital
            })
    
    return {"hospitals": hospital_list, "count": len(hospital_list)}

@router.get("/hospitals/nearby")
def get_nearby_hospitals(
    city: str,
    specialist_only: bool = False,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get nearby hospitals with optional specialist filter.
    
    Quick access to hospitals in a specific city with option to filter for
    thalassemia specialists only.
    
    **Query Parameters:**
    - `city` (str, required): City name to search in
    - `specialist_only` (bool, optional): If true, only returns hospitals with thalassemia specialists (default: False)
    - `limit` (int, optional): Maximum number of results (default: 20)
    
    **Request Examples:**
    ```bash
    GET /api/hospitals/nearby?city=Mumbai&specialist_only=true
    GET /api/hospitals/nearby?city=Delhi&limit=50
    ```
    
    **Response:**
    Same structure as `/api/hospitals/specialist` endpoint
    
    **Use Case:**
    Patient wants to find all hospitals near them, or specifically specialist hospitals.
    """
    if specialist_only:
        return get_thalassemia_specialist_hospitals(city=city, limit=limit, db=db)
    
    profiles = crud.search_profiles(
        db,
        user_type="hospital",
        city=city,
        limit=limit
    )
    
    hospital_list = []
    for profile in profiles:
        hospital = crud.get_hospital(db, str(profile.id))
        if hospital:
            hospital_list.append({
                "profile": profile,
                "hospital_data": hospital
            })
    
    return {"hospitals": hospital_list, "count": len(hospital_list)}

@router.get("/hospitals/by-services")
def get_hospitals_by_services(
    services: str,  # Comma-separated list of services
    city: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get hospitals by their services.
    
    Find hospitals that offer specific services (e.g., Blood Bank, Emergency).
    Useful for patients looking for hospitals with specific facilities.
    
    **Query Parameters:**
    - `services` (str, required): Comma-separated list of services. Each service should be a string.
      Common services: "Emergency", "Surgery", "Blood Bank", "Oncology", "Cardiology", "Pharmacy"
      Example: "Emergency,Surgery" or "Blood Bank"
    - `city` (str, optional): Filter by city name for location-specific results
    - `limit` (int, optional): Maximum number of results (default: 50)
    
    **Request Examples:**
    ```bash
    GET /api/hospitals/by-services?services=Blood%20Bank,Emergency&city=Mumbai
    GET /api/hospitals/by-services?services=Surgery&limit=30
    GET /api/hospitals/by-services?services=Emergency,Oncology,Blood%20Bank
    ```
    
    **Response:**
    Same structure as `/api/hospitals/specialist` endpoint
    
    **Use Case:**
    Patient needs a hospital with Blood Bank facility. Search for hospitals offering this service.
    """
    service_list = [s.strip() for s in services.split(",")]
    
    profiles = crud.search_profiles(
        db,
        user_type="hospital",
        city=city,
        limit=100  # Fetch more to filter
    )
    
    hospital_list = []
    for profile in profiles:
        hospital = crud.get_hospital(db, str(profile.id))
        if hospital and any(service in hospital.services for service in service_list):
            hospital_list.append({
                "profile": profile,
                "hospital_data": hospital
            })
    
    return {"hospitals": hospital_list[:limit], "count": len(hospital_list[:limit])}

@router.get("/resources/for-patient")
def get_resources_for_patient(
    user_id: str,
    blood_type: Optional[str] = None,
    city: Optional[str] = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get personalized resources for a patient based on their needs.
    
    This is the **key endpoint for patient dashboards**. It automatically finds:
    1. Donors with matching blood type and location
    2. Nearby hospitals with thalassemia specialists
    
    **Query Parameters:**
    - `user_id` (str, required): UUID of the patient
    - `blood_type` (str, optional): Override patient's recorded blood type if needed
    - `city` (str, optional): Override patient's city for search
    - `limit` (int, optional): Number of results per resource type (default: 10)
    
    **Request Examples:**
    ```bash
    GET /api/resources/for-patient?user_id=patient-uuid&limit=15
    GET /api/resources/for-patient?user_id=patient-uuid&blood_type=AB+&city=Mumbai
    ```
    
    **Response:**
    - `matched_donors` (list): Donors with compatible blood type and location
    - `specialist_hospitals` (list): Nearby hospitals with thalassemia specialists
    
    Each item in the lists contains `profile` and respective `donor_data` or `hospital_data`.
    
    **Response Example:**
    ```json
    {
        "matched_donors": [
            {
                "profile": {
                    "id": "donor-uuid",
                    "first_name": "Jane",
                    "city": "Mumbai"
                },
                "donor_data": {
                    "blood_type": "O+",
                    "available": true
                }
            }
        ],
        "specialist_hospitals": [
            {
                "profile": {
                    "id": "hospital-uuid",
                    "first_name": "Admin",
                    "city": "Mumbai"
                },
                "hospital_data": {
                    "hospital_name": "City Hospital",
                    "thalassemia_specialist": true,
                    "services": ["Blood Bank", "Emergency"]
                }
            }
        ]
    }
    ```
    
    **Use Case:**
    Patient logs into the app. This single call shows them all relevant resources:
    - Donors they can contact for blood
    - Hospitals they can visit for treatment
    
    **Error Responses:**
    - 404 Not Found: Patient not found
    """
    patient = crud.get_patient(db, user_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Get patient's blood type and location
    required_blood_type = blood_type or patient.blood_type
    patient_city = city or crud.get_profile(db, user_id).city
    
    # Get matching donors
    matching_donors = crud.search_profiles(
        db,
        user_type="donor",
        blood_type=required_blood_type,
        city=patient_city,
        available=True,
        limit=limit
    )
    
    # Get nearby specialist hospitals
    specialist_hospitals = crud.search_profiles(
        db,
        user_type="hospital",
        city=patient_city,
        thalassemia_specialist=True,
        limit=limit
    )
    
    resources = {
        "matched_donors": [],
        "specialist_hospitals": []
    }
    
    for profile in matching_donors:
        donor = crud.get_donor(db, str(profile.id))
        resources["matched_donors"].append({
            "profile": profile,
            "donor_data": donor
        })
    
    for profile in specialist_hospitals:
        hospital = crud.get_hospital(db, str(profile.id))
        resources["specialist_hospitals"].append({
            "profile": profile,
            "hospital_data": hospital
        })
    
    return resources

@router.get("/complete-profile/{user_id}")
def get_complete_profile(user_id: str, db: Session = Depends(get_db)):
    """
    Get complete profile including all related data based on user type.
    
    Retrieves both the basic profile and type-specific data in one call.
    Returns different data structures based on whether the user is a patient, donor, or hospital.
    
    **Path Parameters:**
    - `user_id` (str, required): UUID of the user
    
    **Response for Patient:**
    ```json
    {
        "profile": {
            "id": "uuid",
            "first_name": "John",
            "last_name": "Doe",
            "user_type": "patient",
            "email": "john@example.com"
        },
        "patient_data": {
            "blood_type": "O+",
            "thalassemia_type": "Beta Thalassemia",
            "severity_level": "Moderate"
        }
    }
    ```
    
    **Response for Donor:**
    ```json
    {
        "profile": {...},
        "donor_data": {
            "blood_type": "O+",
            "available": true,
            "total_donations": 8
        }
    }
    ```
    
    **Response for Hospital:**
    ```json
    {
        "profile": {...},
        "hospital_data": {
            "hospital_name": "City Hospital",
            "services": ["Emergency", "Blood Bank"],
            "thalassemia_specialist": true
        }
    }
    ```
    
    **Use Case:**
    Get all information about a user for profile display, contact purposes, or detailed views.
    
    **Error Responses:**
    - 404 Not Found: Profile not found
    """
    profile = crud.get_profile(db, user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    result = {"profile": profile}
    
    if profile.user_type == "patient":
        result["patient_data"] = crud.get_patient(db, user_id)
    elif profile.user_type == "donor":
        result["donor_data"] = crud.get_donor(db, user_id)
    elif profile.user_type == "hospital":
        result["hospital_data"] = crud.get_hospital(db, user_id)
    
    return result

# ==================== Search Endpoints ====================

@router.post("/search")
def search_profiles(request: SearchRequest, db: Session = Depends(get_db)):
    """
    Search for profiles based on various criteria.
    
    Advanced search endpoint with multiple filters. Can search across all user types
    or filter to specific types. Supports location, blood type, availability, and specialist filters.
    
    **Request Body Fields:**
    - `user_type` (str, optional): Filter by "patient", "donor", or "hospital"
    - `blood_type` (str, optional): Filter by blood type (for patients and donors)
    - `city` (str, optional): Filter by city name (partial match)
    - `state` (str, optional): Filter by state/province name (partial match)
    - `thalassemia_specialist` (bool, optional): Filter hospitals by specialist status
    - `available` (bool, optional): Filter donors by availability
    - `limit` (int, optional): Maximum results (default: 50)
    - `offset` (int, optional): Pagination offset (default: 0)
    
    **Request Body Example:**
    ```json
    {
        "user_type": "donor",
        "blood_type": "O+",
        "city": "Mumbai",
        "available": true,
        "limit": 20,
        "offset": 0
    }
    ```
    
    **Response:**
    - `profiles` (list): Array of profile objects matching the criteria
    - `count` (int): Number of profiles found
    
    **Response Example:**
    ```json
    {
        "profiles": [
            {
                "id": "uuid",
                "first_name": "Jane",
                "last_name": "Smith",
                "user_type": "donor",
                "city": "Mumbai"
            }
        ],
        "count": 1
    }
    ```
    """
    profiles = crud.search_profiles(
        db,
        user_type=request.user_type,
        blood_type=request.blood_type,
        city=request.city,
        state=request.state,
        thalassemia_specialist=request.thalassemia_specialist,
        available=request.available,
        limit=request.limit,
        offset=request.offset
    )
    
    return {"profiles": profiles, "count": len(profiles)}

@router.get("/profiles")
def get_all_profiles(user_type: str = None, limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    """
    Get all profiles with optional filtering by user type.
    
    Basic listing endpoint to get all or filtered profiles. Use with pagination
    for large datasets.
    
    **Query Parameters:**
    - `user_type` (str, optional): Filter by "patient", "donor", or "hospital"
    - `limit` (int, optional): Number of results per page (default: 50)
    - `offset` (int, optional): Number of results to skip for pagination (default: 0)
    
    **Request Examples:**
    ```bash
    GET /api/profiles?user_type=donor&limit=50&offset=0
    GET /api/profiles?limit=100
    ```
    
    **Response:**
    - `profiles` (list): Array of profile objects
    - `count` (int): Number of profiles in response
    
    **Use Case:**
    Browse all users, with pagination support.
    """
    profiles = crud.search_profiles(
        db,
        user_type=user_type,
        limit=limit,
        offset=offset
    )
    
    return {"profiles": profiles, "count": len(profiles)}

# ==================== Statistics Endpoints ====================

@router.get("/stats")
def get_statistics(db: Session = Depends(get_db)):
    """
    Get basic statistics for each user type.
    
    Provides overview counts of registered users in the system.
    Useful for dashboards and analytics.
    
    **Response Fields:**
    - `patient_count` (int): Total number of registered patients
    - `donor_count` (int): Total number of registered donors
    - `hospital_count` (int): Total number of registered hospitals
    
    **Response Example:**
    ```json
    {
        "patient_count": 150,
        "donor_count": 75,
        "hospital_count": 25
    }
    ```
    
    **Use Case:**
    Display platform statistics on homepage or admin dashboard.
    """
    stats = crud.get_stats(db)
    return stats

@router.get("/stats/detailed")
def get_detailed_statistics(
    city: Optional[str] = None,
    state: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get detailed statistics with location filtering and resource availability.
    
    Comprehensive statistics including location-based counts and resource availability.
    More detailed than basic stats endpoint.
    
    **Query Parameters:**
    - `city` (str, optional): Filter statistics by city
    - `state` (str, optional): Filter statistics by state/province
    
    **Request Examples:**
    ```bash
    GET /api/stats/detailed?city=Mumbai
    GET /api/stats/detailed?state=Maharashtra
    GET /api/stats/detailed
    ```
    
    **Response Fields:**
    - `patient_count` (int): Total patients in system
    - `donor_count` (int): Total donors in system
    - `hospital_count` (int): Total hospitals in system
    - `filtered_by_location` (object, conditional): If location filters provided:
      - `patient_count` (int): Count in filtered location
      - `donor_count` (int): Count in filtered location
      - `hospital_count` (int): Count in filtered location
    - `location_filter` (object, conditional): Applied filters if any
    - `available_donors_count` (int): Total available donors
    - `thalassemia_specialist_hospitals_count` (int): Hospitals with specialists
    
    **Response Example (with filters):**
    ```json
    {
        "patient_count": 150,
        "donor_count": 75,
        "hospital_count": 25,
        "filtered_by_location": {
            "patient_count": 50,
            "donor_count": 30,
            "hospital_count": 10
        },
        "location_filter": {
            "city": "Mumbai",
            "state": null
        },
        "available_donors_count": 60,
        "thalassemia_specialist_hospitals_count": 15
    }
    ```
    
    **Use Case:**
    Display detailed analytics for a specific region or overall platform health metrics.
    """
    # Base stats
    stats = crud.get_stats(db)
    
    # Add location-specific stats if filters provided
    if city or state:
        filtered_stats = {}
        for user_type in ['patient', 'donor', 'hospital']:
            profiles = crud.search_profiles(
                db,
                user_type=user_type,
                city=city,
                state=state,
                limit=1000
            )
            filtered_stats[f"{user_type}_count"] = len(profiles)
        
        stats['filtered_by_location'] = filtered_stats
        stats['location_filter'] = {"city": city, "state": state}
    
    # Add available donors count
    available_donors = crud.search_profiles(
        db,
        user_type="donor",
        available=True,
        limit=1000
    )
    stats['available_donors_count'] = len(available_donors)
    
    # Add specialist hospitals count
    specialist_hospitals = crud.search_profiles(
        db,
        user_type="hospital",
        thalassemia_specialist=True,
        limit=1000
    )
    stats['thalassemia_specialist_hospitals_count'] = len(specialist_hospitals)
    
    return stats
