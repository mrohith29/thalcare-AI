# Thalcare AI Backend API Documentation

## Overview
This API provides complete user management for three types of users: Patients, Donors, and Hospitals. Each user type has a complete registration flow with profile and user-specific data management.

## Base URL
```
http://127.0.0.1:8000/api
```

## Endpoints

### 1. Authentication

#### POST `/api/login`
Login for any user type.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user_id": "uuid-here",
  "email": "user@example.com",
  "user_type": "patient"
}
```

### 2. Registration

#### POST `/api/register/patient`
Register a new patient with complete profile.

**Request Body:**
```json
{
  "email": "patient@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "1234567890",
  "address": "123 Main St",
  "city": "Mumbai",
  "state": "Maharashtra",
  "country": "India",
  "age": 25,
  "gender": "Male",
  "blood_type": "O+",
  "thalassemia_type": "Beta Thalassemia",
  "severity_level": "Moderate"
}
```

#### POST `/api/register/donor`
Register a new donor with complete profile.

**Request Body:**
```json
{
  "email": "donor@example.com",
  "password": "password123",
  "first_name": "Jane",
  "last_name": "Smith",
  "phone": "9876543210",
  "address": "456 Oak Ave",
  "city": "Mumbai",
  "state": "Maharashtra",
  "country": "India",
  "age": 30,
  "gender": "Female",
  "blood_type": "O+",
  "available": true,
  "contact_preference": "email"
}
```

#### POST `/api/register/hospital`
Register a new hospital with complete profile.

**Request Body:**
```json
{
  "email": "hospital@example.com",
  "password": "password123",
  "first_name": "Admin",
  "last_name": "User",
  "phone": "555-1234",
  "address": "789 Health St",
  "city": "Mumbai",
  "state": "Maharashtra",
  "country": "India",
  "hospital_name": "City Hospital",
  "services": ["Emergency", "Surgery", "Blood Bank"],
  "thalassemia_specialist": true,
  "emergency_contact": "555-9999",
  "website": "https://cityhospital.com"
}
```

### 3. Profile Management

#### GET `/api/profile/{user_id}`
Get a user's profile information.

**Response:**
```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "user_type": "patient",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "1234567890",
  "address": "123 Main St",
  "city": "Mumbai",
  "state": "Maharashtra",
  "country": "India",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

#### PUT `/api/profile/{user_id}`
Update profile information.

**Request Body:**
```json
{
  "first_name": "Updated Name",
  "phone": "9999999999",
  "city": "Delhi"
}
```

### 4. Patient-Specific Endpoints

#### GET `/api/patient/{user_id}`
Get patient-specific data.

#### PUT `/api/patient/{user_id}`
Update patient data.

**Request Body:**
```json
{
  "age": 26,
  "blood_type": "A+",
  "current_requirements": "Regular blood transfusions"
}
```

### 5. Donor-Specific Endpoints

#### GET `/api/donor/{user_id}`
Get donor-specific data.

#### PUT `/api/donor/{user_id}`
Update donor data.

**Request Body:**
```json
{
  "available": false,
  "last_donation_date": "2024-01-15"
}
```

### 6. Hospital-Specific Endpoints

#### GET `/api/hospital/{user_id}`
Get hospital-specific data.

#### PUT `/api/hospital/{user_id}`
Update hospital data.

**Request Body:**
```json
{
  "services": ["Emergency", "Surgery", "Blood Bank", "Cardiology"],
  "thalassemia_specialist": true
}
```

### 7. Search Endpoints

#### POST `/api/search`
Search for profiles with filters.

**Request Body:**
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

#### GET `/api/profiles`
Get all profiles with optional filtering.

**Query Parameters:**
- `user_type` (optional): Filter by patient, donor, or hospital
- `limit` (default: 50): Number of results
- `offset` (default: 0): Pagination offset

### 8. Statistics

#### GET `/api/stats`
Get statistics for each user type.

**Response:**
```json
{
  "patient_count": 150,
  "donor_count": 75,
  "hospital_count": 25
}
```

## Usage Flow

### Complete Registration Flow (Example for Patient):

1. **Register Patient**
   ```bash
   POST /api/register/patient
   ```
   This creates:
   - User account with email and password
   - Profile with basic information
   - Patient-specific record with medical data

2. **Login**
   ```bash
   POST /api/login
   ```
   Returns user_id for subsequent operations

3. **Update Profile**
   ```bash
   PUT /api/profile/{user_id}
   ```

4. **Update Patient Data**
   ```bash
   PUT /api/patient/{user_id}
   ```

## Error Responses

All endpoints return standard HTTP status codes:
- `200 OK` - Success
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication failed
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

Error response format:
```json
{
  "detail": "Error message here"
}
```
