# Thalcare AI - Discovery & Navigation Endpoints

## Overview
These endpoints enable easy discovery and connection between thalassemia patients and resources (donors, hospitals, blood banks). They help reduce search time and connect patients with the right resources quickly.

---

## Donor Discovery Endpoints

### 1. GET `/api/donors/available`
Get all available donors with optional filters.

**Query Parameters:**
- `blood_type` (optional): Filter by blood type (e.g., "O+", "A-")
- `city` (optional): Filter by city
- `state` (optional): Filter by state
- `limit` (default: 50): Number of results
- `offset` (default: 0): Pagination offset

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
        "first_name": "John",
        "last_name": "Doe",
        "city": "Mumbai",
        "phone": "1234567890",
        "user_type": "donor"
      },
      "donor_data": {
        "blood_type": "O+",
        "available": true,
        "last_donation_date": "2024-01-15",
        "total_donations": 5
      }
    }
  ],
  "count": 1
}
```

### 2. GET `/api/donors/nearby`
Get nearby available donors by city.

**Query Parameters:**
- `city` (required): City name
- `blood_type` (optional): Filter by blood type
- `limit` (default: 20): Number of results

**Example Request:**
```bash
GET /api/donors/nearby?city=Mumbai&blood_type=A+
```

### 3. GET `/api/donors/blood-type/{blood_type}`
Get donors by specific blood type.

**Path Parameters:**
- `blood_type` (required): Blood type (e.g., "O+", "B-")

**Query Parameters:**
- `city` (optional): Filter by city
- `limit` (default: 50): Number of results

**Example Request:**
```bash
GET /api/donors/blood-type/O+?city=Delhi
```

---

## Hospital Discovery Endpoints

### 4. GET `/api/hospitals/specialist`
Get hospitals with thalassemia specialists.

**Query Parameters:**
- `city` (optional): Filter by city
- `state` (optional): Filter by state
- `limit` (default: 50): Number of results
- `offset` (default: 0): Pagination offset

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
        "city": "Mumbai",
        "phone": "1234567890"
      },
      "hospital_data": {
        "hospital_name": "City Hospital",
        "thalassemia_specialist": true,
        "services": ["Emergency", "Surgery", "Blood Bank"],
        "rating": 4.5,
        "emergency_contact": "555-9999"
      }
    }
  ],
  "count": 1
}
```

### 5. GET `/api/hospitals/nearby`
Get nearby hospitals.

**Query Parameters:**
- `city` (required): City name
- `specialist_only` (default: false): If true, only returns hospitals with specialists
- `limit` (default: 20): Number of results

**Example Request:**
```bash
GET /api/hospitals/nearby?city=Mumbai&specialist_only=true
```

### 6. GET `/api/hospitals/by-services`
Get hospitals by their services.

**Query Parameters:**
- `services` (required): Comma-separated list of services (e.g., "Emergency,Surgery")
- `city` (optional): Filter by city
- `limit` (default: 50): Number of results

**Example Request:**
```bash
GET /api/hospitals/by-services?services=Blood%20Bank,Emergency&city=Mumbai
```

---

## Personalized Discovery Endpoints

### 7. GET `/api/resources/for-patient`
Get personalized resources for a patient based on their needs.

**Query Parameters:**
- `user_id` (required): Patient's user ID
- `blood_type` (optional): Override patient's blood type
- `city` (optional): Override patient's city
- `limit` (default: 10): Number of results per resource type

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

**Use Case:** A patient logs in and immediately sees donors with matching blood type and nearby specialist hospitals.

### 8. GET `/api/complete-profile/{user_id}`
Get complete profile including all related data based on user type.

**Path Parameters:**
- `user_id` (required): User ID

**Response:**
```json
{
  "profile": {
    "id": "uuid",
    "first_name": "John",
    "user_type": "patient",
    ...
  },
  "patient_data": {
    "blood_type": "O+",
    "thalassemia_type": "Beta Thalassemia",
    ...
  }
}
```

---

## Statistics Endpoints

### 9. GET `/api/stats`
Get basic statistics for each user type.

**Response:**
```json
{
  "patient_count": 150,
  "donor_count": 75,
  "hospital_count": 25
}
```

### 10. GET `/api/stats/detailed`
Get detailed statistics with location filtering.

**Query Parameters:**
- `city` (optional): Filter by city
- `state` (optional): Filter by state

**Example Request:**
```bash
GET /api/stats/detailed?city=Mumbai
```

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

## Usage Scenarios

### Scenario 1: Patient Looking for Blood Donors
```bash
# Step 1: Find donors with matching blood type nearby
GET /api/donors/nearby?city=Mumbai&blood_type=O+&limit=10

# Step 2: Get contact details
GET /api/complete-profile/{donor_id}
```

### Scenario 2: Patient Finding Specialist Hospital
```bash
# Find thalassemia specialist hospitals in city
GET /api/hospitals/specialist?city=Mumbai&limit=20

# Get hospital details
GET /api/complete-profile/{hospital_id}
```

### Scenario 3: Patient Dashboard - Quick Resources
```bash
# Get all personalized resources in one call
GET /api/resources/for-patient?user_id={patient_id}&limit=10
```

### Scenario 4: Finding Hospitals with Specific Services
```bash
# Find hospitals with Blood Bank and Emergency services
GET /api/hospitals/by-services?services=Blood%20Bank,Emergency&city=Mumbai
```

### Scenario 5: Browse All Available Donors
```bash
# Get all available donors with filters
GET /api/donors/available?blood_type=AB+&state=Maharashtra&limit=50
```

---

## Key Features

1. **Location-Based Discovery**: Find resources by city and state
2. **Blood Type Matching**: Filter donors by specific blood types
3. **Availability Filtering**: Only show available donors
4. **Specialist Filtering**: Find hospitals with thalassemia specialists
5. **Service-Based Search**: Find hospitals by their services
6. **Personalized Recommendations**: Get resources tailored to patient needs
7. **Complete Profile Views**: Get all details including profile and type-specific data
8. **Statistics & Analytics**: Track resources and availability

---

## Common Use Cases

### Patient Journey
1. **Login** → `/api/login`
2. **View Personalized Resources** → `/api/resources/for-patient?user_id={id}`
3. **Explore Donor Options** → `/api/donors/available?blood_type={type}&city={city}`
4. **Find Hospitals** → `/api/hospitals/specialist?city={city}`
5. **Get Details** → `/api/complete-profile/{user_id}`

### Donor Journey
1. **Register as Donor** → `/api/register/donor`
2. **Update Availability** → `/api/donor/{id}` (PUT)
3. **Check Stats** → `/api/stats/detailed`

### Hospital Journey
1. **Register Hospital** → `/api/register/hospital`
2. **Update Services** → `/api/hospital/{id}` (PUT)
3. **View Statistics** → `/api/stats/detailed?city={city}`
