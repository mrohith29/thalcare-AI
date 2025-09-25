-- =====================================================
-- ThalCare AI - Simplified Database Schema
-- Clean inheritance from auth.users table
-- =====================================================

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- 1. COMMON PROFILES TABLE (inherits from auth.users)
-- =====================================================
CREATE TABLE profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    user_type TEXT NOT NULL CHECK (user_type IN ('patient', 'donor', 'doctor', 'hospital')),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    country TEXT DEFAULT 'India',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 2. PATIENTS TABLE (inherits from profiles)
-- =====================================================
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

-- =====================================================
-- 3. DONORS TABLE (inherits from profiles)
-- =====================================================
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

-- =====================================================
-- 4. DOCTORS TABLE (inherits from profiles)
-- =====================================================
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

-- =====================================================
-- 5. HOSPITALS TABLE (inherits from profiles)
-- =====================================================
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

-- =====================================================
-- 6. BLOOD REQUESTS TABLE
-- =====================================================
CREATE TABLE blood_requests (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    blood_type TEXT NOT NULL CHECK (blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    urgency_level TEXT DEFAULT 'normal' CHECK (urgency_level IN ('emergency', 'urgent', 'high', 'normal', 'low')),
    units_needed INTEGER DEFAULT 1 CHECK (units_needed > 0),
    needed_by_date DATE NOT NULL,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'fulfilled', 'expired', 'cancelled')),
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Ensure needed_by_date is in the future when creating
    CONSTRAINT future_date_check CHECK (needed_by_date >= CURRENT_DATE)
);

-- =====================================================
-- 7. APPOINTMENTS TABLE
-- =====================================================
CREATE TABLE appointments (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    patient_id UUID NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    doctor_id UUID REFERENCES doctors(id) ON DELETE SET NULL,
    hospital_id UUID REFERENCES hospitals(id) ON DELETE SET NULL,
    appointment_date TIMESTAMP WITH TIME ZONE NOT NULL,
    appointment_type TEXT DEFAULT 'consultation' CHECK (appointment_type IN ('consultation', 'checkup', 'emergency', 'followup')),
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'completed', 'cancelled', 'no_show')),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Ensure appointment_date is in the future when creating
    CONSTRAINT future_appointment_check CHECK (appointment_date > NOW())
);

-- =====================================================
-- 8. BLOOD DONATIONS TABLE
-- =====================================================
CREATE TABLE blood_donations (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
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

-- =====================================================
-- 9. MESSAGES TABLE (for communication between users)
-- =====================================================
CREATE TABLE messages (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    sender_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    receiver_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Profiles indexes
CREATE INDEX idx_profiles_user_type ON profiles(user_type);
CREATE INDEX idx_profiles_email ON profiles(email);
CREATE INDEX idx_profiles_city_state ON profiles(city, state);

-- Patients indexes
CREATE INDEX idx_patients_blood_type ON patients(blood_type);
CREATE INDEX idx_patients_thalassemia_type ON patients(thalassemia_type);
CREATE INDEX idx_patients_severity ON patients(severity_level);

-- Donors indexes
CREATE INDEX idx_donors_blood_type ON donors(blood_type);
CREATE INDEX idx_donors_available ON donors(available);
CREATE INDEX idx_donors_last_donation ON donors(last_donation_date);

-- Doctors indexes
CREATE INDEX idx_doctors_specialization ON doctors(specialization);
CREATE INDEX idx_doctors_available ON doctors(available);
CREATE INDEX idx_doctors_thalassemia_specialist ON doctors(thalassemia_specialist);

-- Hospitals indexes
CREATE INDEX idx_hospitals_thalassemia_specialist ON hospitals(thalassemia_specialist);
CREATE INDEX idx_hospitals_rating ON hospitals(rating);
CREATE INDEX idx_hospitals_services ON hospitals USING GIN(services);

-- Blood requests indexes
CREATE INDEX idx_blood_requests_status ON blood_requests(status);
CREATE INDEX idx_blood_requests_urgency ON blood_requests(urgency_level);
CREATE INDEX idx_blood_requests_blood_type ON blood_requests(blood_type);
CREATE INDEX idx_blood_requests_needed_by ON blood_requests(needed_by_date);

-- Appointments indexes
CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_appointments_doctor ON appointments(doctor_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_appointments_status ON appointments(status);

-- Messages indexes
CREATE INDEX idx_messages_sender ON messages(sender_id);
CREATE INDEX idx_messages_receiver ON messages(receiver_id);
CREATE INDEX idx_messages_created ON messages(created_at);

-- =====================================================
-- TRIGGERS FOR AUTOMATIC UPDATES
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers to all tables
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_patients_updated_at BEFORE UPDATE ON patients FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_donors_updated_at BEFORE UPDATE ON donors FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_doctors_updated_at BEFORE UPDATE ON doctors FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_hospitals_updated_at BEFORE UPDATE ON hospitals FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_blood_requests_updated_at BEFORE UPDATE ON blood_requests FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_appointments_updated_at BEFORE UPDATE ON appointments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_blood_donations_updated_at BEFORE UPDATE ON blood_donations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to update donor total donations
CREATE OR REPLACE FUNCTION update_donor_total_donations()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE donors 
        SET total_donations = total_donations + NEW.units_donated,
            last_donation_date = NEW.donation_date
        WHERE id = NEW.donor_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_donor_donations 
    AFTER INSERT ON blood_donations 
    FOR EACH ROW EXECUTE FUNCTION update_donor_total_donations();

-- =====================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- =====================================================

-- Enable RLS on all tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE donors ENABLE ROW LEVEL SECURITY;
ALTER TABLE doctors ENABLE ROW LEVEL SECURITY;
ALTER TABLE hospitals ENABLE ROW LEVEL SECURITY;
ALTER TABLE blood_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE blood_donations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Users can view their own profile" ON profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update their own profile" ON profiles FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Users can insert their own profile" ON profiles FOR INSERT WITH CHECK (auth.uid() = id);

-- Public read policies for finding users
CREATE POLICY "Anyone can view patients" ON patients FOR SELECT USING (true);
CREATE POLICY "Anyone can view donors" ON donors FOR SELECT USING (true);
CREATE POLICY "Anyone can view doctors" ON doctors FOR SELECT USING (true);
CREATE POLICY "Anyone can view hospitals" ON hospitals FOR SELECT USING (true);

-- Patients policies
CREATE POLICY "Patients can update their own data" ON patients FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Patients can insert their own data" ON patients FOR INSERT WITH CHECK (auth.uid() = id);

-- Donors policies
CREATE POLICY "Donors can update their own data" ON donors FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Donors can insert their own data" ON donors FOR INSERT WITH CHECK (auth.uid() = id);

-- Doctors policies
CREATE POLICY "Doctors can update their own data" ON doctors FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Doctors can insert their own data" ON doctors FOR INSERT WITH CHECK (auth.uid() = id);

-- Hospitals policies
CREATE POLICY "Hospitals can update their own data" ON hospitals FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Hospitals can insert their own data" ON hospitals FOR INSERT WITH CHECK (auth.uid() = id);

-- Blood requests policies
CREATE POLICY "Anyone can view blood requests" ON blood_requests FOR SELECT USING (true);
CREATE POLICY "Patients can create blood requests" ON blood_requests FOR INSERT WITH CHECK (auth.uid() = patient_id);
CREATE POLICY "Patients can update their own requests" ON blood_requests FOR UPDATE USING (auth.uid() = patient_id);

-- Appointments policies
CREATE POLICY "Users can view their own appointments" ON appointments FOR SELECT USING (auth.uid() = patient_id OR auth.uid() = doctor_id);
CREATE POLICY "Patients can create appointments" ON appointments FOR INSERT WITH CHECK (auth.uid() = patient_id);
CREATE POLICY "Users can update their own appointments" ON appointments FOR UPDATE USING (auth.uid() = patient_id OR auth.uid() = doctor_id);

-- Messages policies
CREATE POLICY "Users can view their own messages" ON messages FOR SELECT USING (auth.uid() = sender_id OR auth.uid() = receiver_id);
CREATE POLICY "Users can send messages" ON messages FOR INSERT WITH CHECK (auth.uid() = sender_id);
CREATE POLICY "Users can update their own messages" ON messages FOR UPDATE USING (auth.uid() = sender_id OR auth.uid() = receiver_id);

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- View for available blood donors
CREATE VIEW available_donors AS
SELECT 
    p.id,
    p.first_name,
    p.last_name,
    p.email,
    p.phone,
    p.address,
    p.city,
    p.state,
    d.blood_type,
    d.last_donation_date,
    d.total_donations
FROM profiles p
JOIN donors d ON p.id = d.id
WHERE d.available = true 
AND p.is_active = true
AND (d.last_donation_date IS NULL OR d.last_donation_date < CURRENT_DATE - INTERVAL '56 days');

-- View for thalassemia specialists
CREATE VIEW thalassemia_specialists AS
SELECT 
    p.id,
    p.first_name,
    p.last_name,
    p.email,
    p.phone,
    p.address,
    p.city,
    p.state,
    d.specialization,
    d.experience_years,
    d.consultation_fee,
    d.languages
FROM profiles p
JOIN doctors d ON p.id = d.id
WHERE d.thalassemia_specialist = true 
AND d.available = true
AND p.is_active = true;

-- View for thalassemia hospitals
CREATE VIEW thalassemia_hospitals AS
SELECT 
    p.id,
    p.first_name,
    p.last_name,
    p.email,
    p.phone,
    p.address,
    p.city,
    p.state,
    h.hospital_name,
    h.services,
    h.rating,
    h.total_ratings,
    h.emergency_contact
FROM profiles p
JOIN hospitals h ON p.id = h.id
WHERE h.thalassemia_specialist = true 
AND p.is_active = true;

-- View for active blood requests
CREATE VIEW active_blood_requests AS
SELECT 
    br.id,
    br.blood_type,
    br.urgency_level,
    br.units_needed,
    br.needed_by_date,
    p.first_name,
    p.last_name,
    p.city,
    p.state,
    pat.thalassemia_type,
    pat.severity_level,
    br.created_at
FROM blood_requests br
JOIN patients pat ON br.patient_id = pat.id
JOIN profiles p ON pat.id = p.id
WHERE br.status = 'active'
AND br.needed_by_date >= CURRENT_DATE;

-- =====================================================
-- COMMENTS FOR DOCUMENTATION
-- =====================================================

COMMENT ON TABLE profiles IS 'Common user profiles inheriting from auth.users table';
COMMENT ON TABLE patients IS 'Patient-specific information for thalassemia patients';
COMMENT ON TABLE donors IS 'Blood donor information and availability';
COMMENT ON TABLE doctors IS 'Doctor profiles with specializations';
COMMENT ON TABLE hospitals IS 'Hospital information and services';
COMMENT ON TABLE blood_requests IS 'Blood donation requests from patients';
COMMENT ON TABLE appointments IS 'Medical appointments between patients and doctors';
COMMENT ON TABLE blood_donations IS 'Blood donation records';
COMMENT ON TABLE messages IS 'Communication between users';

-- =====================================================
-- SAMPLE DATA INSERTION (Optional)
-- =====================================================

-- Note: This section can be uncommented to insert sample data for testing
/*
-- Sample hospital
INSERT INTO profiles (id, user_type, first_name, last_name, email, phone, city, state) 
VALUES (uuid_generate_v4(), 'hospital', 'Apollo', 'Hospital', 'apollo@example.com', '1234567890', 'Mumbai', 'Maharashtra');

-- Sample doctor
INSERT INTO profiles (id, user_type, first_name, last_name, email, phone, city, state) 
VALUES (uuid_generate_v4(), 'doctor', 'Dr. John', 'Doe', 'john.doe@example.com', '9876543210', 'Mumbai', 'Maharashtra');

-- Sample patient
INSERT INTO profiles (id, user_type, first_name, last_name, email, phone, city, state) 
VALUES (uuid_generate_v4(), 'patient', 'Jane', 'Smith', 'jane.smith@example.com', '5555555555', 'Mumbai', 'Maharashtra');

-- Sample donor
INSERT INTO profiles (id, user_type, first_name, last_name, email, phone, city, state) 
VALUES (uuid_generate_v4(), 'donor', 'Mike', 'Johnson', 'mike.johnson@example.com', '1111111111', 'Mumbai', 'Maharashtra');
*/ 