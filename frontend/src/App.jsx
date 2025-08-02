import { useState } from 'react'
import { useNavigate, Routes, Route } from 'react-router-dom'
import PatientRegistration from "./register/patient-registration"
import DonorRegistration from "./register/donor-registration"
import HospitalRegistration from "./register/hospital-registration"
import ExpertDoctorRegistration from "./register/expert-doctor-registration"

import './App.css'

function Home() {
  const navigate = useNavigate()

  return (
    <>
      <h2>How do you want to create your Account?</h2>

      <button onClick={() => navigate('/register/patient')}>Register as a Patient</button>
      <br /><br />
      <button onClick={() => navigate('/register/donor')}>Register as a Donor</button>
      <br /><br />
      <button onClick={() => navigate('/register/hospital')}>Register as a Hospital</button>
      <br /><br />
      <button onClick={() => navigate('/register/doctor')}>Register as an Expert Doctor</button>
    </>
  )
}

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register/patient" element={<PatientRegistration />} />
        <Route path="/register/donor" element={<DonorRegistration />} />
        <Route path="/register/hospital" element={<HospitalRegistration />} />
        <Route path="/register/doctor" element={<ExpertDoctorRegistration />} />
      </Routes>
    </>
  )
}

export default App
