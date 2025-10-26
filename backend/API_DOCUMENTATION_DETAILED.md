# Thalcare AI API - Detailed Documentation

## Base URL
```
http://127.0.0.1:8000/api
```

---

## 1. Authentication Endpoints

### POST `/api/login`
Authenticate a user and return user information.

**Description:**  
Validates user credentials (email and password) and returns user ID, email, and user type. Works for all user types: patients, donors, and hospitals.

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

**Response Fields:**
- `message` (str): Success message
- `user_id` (str): UUID of the authenticated user
- `email` (str): User's email address
- `user_type` (str): Type of user - either "patient", "donor", or "hospital"

**Success Response (200 OK):**
```json
{
    "message": "Login successful",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "patient@example.com",
    "user_type": "patient"
}
```

**Error Response (401 Unauthorized):**
```json
{
    "detail": "Invalid email or password"
}
```

---

## 2. Registration Endpoints

### POST `/api/register/patient`
Register a new patient user with complete profile and medical information.

**Description:**  
Creates a new patient account with all related data including user credentials, profile information, and patient-specific medical data.

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
- `blood_type` (str, optional): Blood group (e.g., "O+", "A-", "B+", "AB+")
- `thalassemia_type` (str, optional): Type of thalassemia (e.g., "Alpha", "Beta")
- `severity_level` (str, optional): Severity ("Mild", "Moderate", "Severe")
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

**Response Fields:**
- `message` (str): Success message
- `user_id` (str): UUID of the newly created user
- `email` (str): Registered email address

**Success Response (200 OK):**
```json
{
    "message": "Patient registered successfully",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john.patient@example.com"
}
```

**Error Response (400 Bad Request):**
```json
{
    "detail": "Email already registered"
}
```

---

### POST `/api/register/donor`
Register a new donor user with complete profile and donation information.

**Description:**  
Creates a new donor account with user credentials, profile information, and donor-specific data.

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
- `country` (str, optional): Defaults to "India"

*Donor Specific Fields:*
- `age` (int, optional): Donor's age
- `gender` (str, optional): Gender
- `blood_type` (str, optional): Blood group
- `last_donation_date` (date, optional): Date of last donation (YYYY-MM-DD)
- `total_donations` (int, optional): Total number of donations (defaults to 0)
- `available` (bool, optional): Currently available for donation (defaults to True)
- `contact_preference` (str, optional): How to contact ("email", "phone", "both", defaults to "email")
- `emergency_contact` (bool, optional): Available for emergency donations (defaults to False)
- `health_conditions` (list[str], optional): List of health conditions

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

**Success Response (200 OK):**
```json
{
    "message": "Donor registered successfully",
    "user_id": "660e8400-e29b-41d4-a716-446655440000",
    "email": "donor.jane@example.com"
}
```

---

### POST `/api/register/hospital`
Register a new hospital user with complete profile and hospital information.

**Description:**  
Creates a new hospital account with user credentials, profile information, and hospital-specific data.

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
- `country` (str, optional): Defaults to "India"

*Hospital Specific Fields:*
- `hospital_name` (str, required): Official hospital name
- `services` (list[str], optional): List of services offered
- `thalassemia_specialist` (bool, optional): Has thalassemia specialists (defaults to False)
- `rating` (float, optional): Average rating (defaults to 0.0)
- `total_ratings` (int, optional): Number of ratings (defaults to 0)
- `emergency_contact` (str, optional): Emergency contact number
- `website` (str, optional): Hospital website URL
- `insurance_accepted` (list[str], optional): Accepted insurance providers

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

**Success Response (200 OK):**
```json
{
    "message": "Hospital registered successfully",
    "user_id": "770e8400-e29b-41d4-a716-446655440000",
    "email": "admin@cityhospital.com"
}
```

---

## 3. Profile Management Endpoints

### GET `/api/profile/{user_id}`
Get a user's profile information.

**Description:**  
Retrieves basic profile information for any user type.

**Path Parameters:**
- `user_id` (str, required): UUID of the user

**Response Fields:**
- `id` (str): User's UUID
- `email` (str): Email address
- `user_type` (str): Type of user
- `first_name` (str): First name
- `last_name` (str): Last name
- `phone` (str, nullable): Phone number
- `address` (str, nullable): Address
- `city` (str, nullable): City
- `state` (str, nullable): State
- `country` (str): Country
- `is_active` (bool): Account active status
- `created_at` (str): Creation timestamp

**Success Response (200 OK):**
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

**Error Response (404 Not Found):**
```json
{
    "detail": "Profile not found"
}
```

---

### PUT `/api/profile/{user_id}`
Update a user's profile information.

**Description:**  
Allows updating any profile field. Only provided fields will be updated.

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

**Success Response (200 OK):**
```json
{
    "message": "Profile updated successfully"
}
```

---

## 4. Type-Specific Endpoints

### GET `/api/patient/{user_id}`
Get patient-specific medical data.

**Description:**  
Retrieves detailed medical information for a patient.

**Response Fields:**
- `id` (str): Patient's user ID
- `age` (int, nullable): Age
- `gender` (str, nullable): Gender
- `blood_type` (str, nullable): Blood group
- `thalassemia_type` (str, nullable): Type of thalassemia
- `severity_level` (str, nullable): Severity
- `diagnosis_date` (date, nullable): Diagnosis date
- `current_requirements` (str, nullable): Treatment needs
- `emergency_contact_name` (str, nullable): Emergency contact name
- `emergency_contact_phone` (str, nullable): Emergency contact phone
- `insurance_provider` (str, nullable): Insurance provider

**Success Response (200 OK):**
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

---

### GET `/api/donor/{user_id}`
Get donor-specific donation information.

**Response Fields:**
- `id` (str): Donor's user ID
- `age` (int, nullable): Age
- `gender` (str, nullable): Gender
- `blood_type` (str, nullable): Blood group
- `last_donation_date` (date, nullable): Last donation date
- `total_donations` (int): Total donations
- `available` (bool): Availability status
- `contact_preference` (str): Contact method
- `emergency_contact` (bool): Emergency availability
- `health_conditions` (list[str]): Health conditions

**Success Response (200 OK):**
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

---

### GET `/api/hospital/{user_id}`
Get hospital-specific information.

**Response Fields:**
- `id` (str): Hospital's user ID
- `hospital_name` (str): Hospital name
- `services` (list[str]): Services offered
- `thalassemia_specialist` (bool): Has specialists
- `rating` (float): Average rating
- `total_ratings` (int): Number of ratings
- `emergency_contact` (str, nullable): Emergency contact
- `website` (str, nullable): Website URL
- `insurance_accepted` (list[str]): Accepted insurance

**Success Response (200 OK):**
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

---

## 5. Discovery Endpoints

### GET `/api/donors/available`
Get list of available donors with filters.

**Description:**  
Retrieves donors who are currently available with comprehensive filtering options.

**Query Parameters:**
- `blood_type` (str, optional): Filter by blood type (e.g., "O+", "A-")
- `city` (str, optional): Filter by city (partial match)
- `state` (str, optional): Filter by state (partial match)
- `limit` (int, optional): Max results (default: 50)
- `offset` (int, optional): Pagination offset (default: 0)

**Example Request:**
```bash
GET /api/donors/available?blood_type=O+&city=Mumbai&limit=20
```

**Response:**
```json
{
    "donors": [
        {
            "profile": {
                "id": "uuid",
                "first_name": "Jane",
                "last_name": "Smith",
                "city": "Mumbai",
                "phone": "9876543220"
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

---

### GET `/api/donors/nearby?city={city_name}&blood_type={blood_type}`
Get nearby available donors by city.

**Query Parameters:**
- `city` (str, required): City name
- `blood_type` (str, optional): Filter by blood type
- `limit` (int, optional): Max results (default: 20)

**Example Request:**
```bash
GET /api/donors/nearby?city=Mumbai&blood_type=A+
```

---

### GET `/api/donors/blood-type/{blood_type}`
Get donors by specific blood type.

**Path Parameters:**
- `blood_type` (str, required): Blood type (e.g., "O+", "B-")

**Query Parameters:**
- `city` (str, optional): Filter by city
- `limit` (int, optional): Max results (default: 50)

**Example Request:**
```bash
GET /api/donors/blood-type/O+?city=Delhi
```

---

### GET `/api/hospitals/specialist`
Get hospitals with thalassemia specialists.

**Query Parameters:**
- `city` (str, optional): Filter by city
- `state` (str, optional): Filter by state
- `limit` (int, optional): Max results (default: 50)
- `offset` (int, optional): Pagination offset (default: 0)

**Example Request:**
```bash
GET /api/hospitals/specialist?city=Mumbai&state=Maharashtra
```

**Response:**
```json
{
    "hospitals": [
        {
            "profile": {
                "id": "uuid",
                "first_name": "Admin",
                "city": "Mumbai"
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

---

### GET `/api/hospitals/nearby?city={city_name}&specialist_only={boolean}`
Get nearby hospitals.

**Query Parameters:**
- `city` (str, required): City name
- `specialist_only` (bool, optional): Only return specialist hospitals (default: False)
- `limit` (int, optional): Max results (default: 20)

**Example Request:**
```bash
GET /api/hospitals/nearby?city=Mumbai&specialist_only=true
```

---

### GET `/api/hospitals/by-services?services={services_list}&city={city_name}`
Get hospitals by their services.

**Query Parameters:**
- `services` (str, required): Comma-separated services (e.g., "Emergency,Surgery")
- `city` (str, optional): Filter by city
- `limit` (int, optional): Max results (default: 50)

**Example Request:**
```bash
GET /api/hospitals/by-services?services=Blood%20Bank,Emergency&city=Mumbai
```

---

### GET `/api/resources/for-patient?user_id={patient_id}&blood_type={type}&city={city}&limit={number}`
Get personalized resources for a patient.

**Description:**  
**Key endpoint for patient dashboards.** Automatically finds matching donors and specialist hospitals.

**Query Parameters:**
- `user_id` (str, required): Patient's UUID
- `blood_type` (str, optional): Override patient's blood type
- `city` (str, optional): Override patient's city
- `limit` (int, optional): Results per resource type (default: 10)

**Example Request:**
```bash
GET /api/resources/for-patient?user_id=patient-uuid&limit=15
```

**Response:**
```json
{
    "matched_donors": [
        {
            "profile": {...},
            "donor_data": {...}
        }
    ],
    "specialist_hospitals": [
        {
            "profile": {...},
            "hospital_data": {...}
        }
    ]
}
```

---

### GET `/api/complete-profile/{user_id}`
Get complete profile with type-specific data.

**Description:**  
Retrieves both basic profile and type-specific data in one call.

**Path Parameters:**
- `user_id` (str, required): UUID of the user

**Response for Patient:**
```json
{
    "profile": {
        "id": "uuid",
        "first_name": "John",
        "user_type": "patient",
        "email": "john@example.com"
    },
    "patient_data": {
        "blood_type": "O+",
        "thalassemia_type": "Beta Thalassemia"
    }
}
```

---

## 6. Search Endpoints

### POST `/api/search`
Search profiles with multiple criteria.

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

---

### GET `/api/profiles`
Get all profiles with optional filtering.

**Query Parameters:**
- `user_type` (str, optional): Filter by type
- `limit` (int, optional): Max results (default: 50)
- `offset` (int, optional): Pagination offset (default: 0)

---

## 7. Statistics Endpoints

### GET `/api/stats`
Get basic statistics.

**Response:**
```json
{
    "patient_count": 150,
    "donor_count": 75,
    "hospital_count": 25
}
```

---

### GET `/api/stats/detailed?city={city}&state={state}`
Get detailed statistics with location filtering.

**Query Parameters:**
- `city` (str, optional): Filter by city
- `state` (str, optional): Filter by state

**Response:**
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

---

## Error Responses

All endpoints return standard HTTP status codes:
- **200 OK**: Success
- **400 Bad Request**: Invalid input or email already exists
- **401 Unauthorized**: Authentication failed
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

Error response format:
```json
{
    "detail": "Error message here"
}
```

---

## API Testing

The FastAPI framework provides interactive API documentation:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
