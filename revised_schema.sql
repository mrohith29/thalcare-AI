-- Enable uuid-ossp extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (basic authentication info)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Profiles table linked to users (common user info)
CREATE TABLE profiles (
    id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    user_type TEXT NOT NULL CHECK (user_type IN ('patient', 'donor', 'doctor', 'hospital')),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    country TEXT DEFAULT 'India',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Patients table (extends profiles)
CREATE TABLE patients (
    id UUID PRIMARY KEY REFERENCES profiles(id) ON DELETE CASCADE,
    age INTEGER CHECK (age > 0 AND age < 150),
    gender TEXT CHECK (gender IN ('male', 'female', 'other')),
    blood_type TEXT CHECK (blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    thalassemia_type TEXT CHECK (thalassemia_type IN ('alpha', 'beta', 'delta-beta', 'gamma-delta-beta')),
    severity_level TEXT CHECK (severity_level IN ('minor', 'intermedia', 'major')),
    diagnosis_date DATE,
    current_requirements TEXT,
    emergency_contact_name TEXT,
    emergency_contact_phone TEXT,
    insurance_provider TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Donors table (extends profiles)
CREATE TABLE donors (
    id UUID PRIMARY KEY REFERENCES profiles(id) ON DELETE CASCADE,
    age INTEGER CHECK (age >= 18 AND age < 150),
    gender TEXT CHECK (gender IN ('male', 'female', 'other')),
    blood_type TEXT CHECK (blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    last_donation_date DATE,
    total_donations INTEGER DEFAULT 0,
    available BOOLEAN DEFAULT true,
    contact_preference TEXT DEFAULT 'email' CHECK (contact_preference IN ('email', 'phone', 'both')),
    emergency_contact BOOLEAN DEFAULT false,
    health_conditions TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Doctors table (extends profiles)
CREATE TABLE doctors (
    id UUID PRIMARY KEY REFERENCES profiles(id) ON DELETE CASCADE,
    specialization TEXT NOT NULL,
    experience_years INTEGER CHECK (experience_years >= 0),
    license_number TEXT UNIQUE,
    medical_council TEXT,
    available BOOLEAN DEFAULT true,
    consultation_fee DECIMAL(10, 2),
    languages TEXT[],
    thalassemia_specialist BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Hospitals table (extends profiles)
CREATE TABLE hospitals (
    id UUID PRIMARY KEY REFERENCES profiles(id) ON DELETE CASCADE,
    hospital_name TEXT NOT NULL,
    services TEXT[] DEFAULT '{}',
    thalassemia_specialist BOOLEAN DEFAULT false,
    rating DECIMAL(3, 2) DEFAULT 0.00 CHECK (rating >= 0 AND rating <= 5),
    total_ratings INTEGER DEFAULT 0,
    emergency_contact TEXT,
    website TEXT,
    insurance_accepted TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Blood Requests
CREATE TABLE blood_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    blood_type TEXT NOT NULL CHECK (blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    urgency_level TEXT DEFAULT 'normal' CHECK (urgency_level IN ('emergency', 'urgent', 'high', 'normal', 'low')),
    units_needed INTEGER DEFAULT 1 CHECK (units_needed > 0),
    needed_by_date DATE NOT NULL,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'fulfilled', 'expired', 'cancelled')),
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT future_date_check CHECK (needed_by_date >= CURRENT_DATE)
);

-- Appointments
CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    doctor_id UUID REFERENCES doctors(id) ON DELETE SET NULL,
    hospital_id UUID REFERENCES hospitals(id) ON DELETE SET NULL,
    appointment_date TIMESTAMP WITH TIME ZONE NOT NULL,
    appointment_type TEXT DEFAULT 'consultation' CHECK (appointment_type IN ('consultation', 'checkup', 'emergency', 'followup')),
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'completed', 'cancelled', 'no_show')),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT future_appointment_check CHECK (appointment_date > NOW())
);

-- Blood Donations
CREATE TABLE blood_donations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    donor_id UUID NOT NULL REFERENCES donors(id) ON DELETE CASCADE,
    hospital_id UUID REFERENCES hospitals(id) ON DELETE SET NULL,
    donation_date DATE NOT NULL,
    blood_type TEXT NOT NULL CHECK (blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    units_donated INTEGER DEFAULT 1 CHECK (units_donated > 0),
    status TEXT DEFAULT 'completed' CHECK (status IN ('scheduled', 'completed', 'cancelled', 'deferred')),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Messages
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sender_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    receiver_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
