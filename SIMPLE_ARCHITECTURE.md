# ThalCare AI - Simple Web Architecture

## Overview
A simple web application for thalassemia patients to find hospitals, book appointments, and connect with blood donors using React.js + FastAPI + Supabase.

## Core Features
1. **User Authentication** (Login/Register)
2. **Hospital Finder** (Location-based search)
3. **Appointment Booking**
4. **Blood Donor Search**
5. **User Profile Management**
6. **Simple AI Chatbot** (Rule-based responses)

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
- **Python libraries**: pandas, requests, geopy
- **Simple AI**: Rule-based chatbot responses

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
