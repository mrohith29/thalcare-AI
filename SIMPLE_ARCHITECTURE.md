# ThalCare AI - Simple Web Architecture

## Overview
A simple web application for thalassemia patients to find hospitals, book appointments, and connect with blood donors using React.js + FastAPI + Supabase.

## Core Features
1. **User Authentication** (Login/Register)
2. **AI-Powered Hospital Finder** (Smart recommendations based on symptoms & location)
3. **AI Appointment Scheduling** (Best time/doctor suggestions)
4. **AI Blood Donor Matching** (Intelligent donor-patient pairing)
5. **AI Health Assistant** (Symptom analysis & treatment advice)
6. **User Profile Management**

## Technology Stack

### Frontend
- **React.js** 
- **Tailwind CSS** for styling
- **React Router** for navigation
- **Axios** for API calls
- **React Hook Form** for forms

### Backend
- **Python FastAPI** (REST API)
- **Supabase** (Database + Authentication)
- **AI/ML Libraries**: scikit-learn, transformers, openai
- **Python libraries**: pandas, requests, geopy

### Database (Supabase)
- **PostgreSQL** (managed by Supabase)
- **Real-time subscriptions**
- **Built-in Authentication**
- **Row Level Security (RLS)**

## Architecture Diagram

```
┌─────────────────────────────────────────┐
│            React.js Frontend            │
│        (Tailwind CSS + TypeScript)      │
└─────────────────┬───────────────────────┘
                  │ HTTP/REST API
┌─────────────────▼───────────────────────┐
│           FastAPI Backend               │
│         (Python + Pydantic)            │
└─────────────────┬───────────────────────┘
                  │ SQL + Auth
┌─────────────────▼───────────────────────┐
│             Supabase                    │
│    (PostgreSQL + Auth + Real-time)     │
└─────────────────────────────────────────┘
```

## User Flow

### 1. Authentication Flow
```
User → Register/Login → Profile Setup → Dashboard
```

### 2. AI Hospital Search Flow
```
Dashboard → Symptom Input → AI Analysis → Smart Hospital Recommendations → Book Appointment
```

### 3. AI Blood Donor Flow
```
Dashboard → Blood Request → AI Matching → Priority Donor List → Auto Contact
```

### 4. AI Health Assistant Flow
```
Dashboard → Chat → Symptom Analysis → Treatment Advice → Doctor Referral
```

### 4. Appointment Management Flow
```
Dashboard → My Appointments → View/Cancel → Reschedule
```

## User Access Features

### Guest User
- View home page
- Register/Login

### Authenticated Patient
- AI-powered hospital search with symptom analysis
- Smart appointment booking with optimal scheduling
- AI blood donor matching with priority ranking
- Intelligent health assistant with personalized advice
- Manage appointment history
- Update profile
- Receive AI-generated health insights

### Blood Donor
- Register as donor with AI compatibility scoring
- AI-powered donation scheduling optimization
- Respond to prioritized blood requests
- View donation history with health impact metrics
