import { useState } from 'react'
import { useNavigate, Routes, Route } from 'react-router-dom'
import DynamicSignup from "./register/signup"
import './App.css'

function Home() {
  const navigate = useNavigate()

  return (
    <>
      <h2>How do you want to create your Account?</h2>

      <button onClick={() => navigate('/register/signup')}>Register as a Patient</button>
    </>
  )
}

function App() {
  return (
    <>
      <Routes>
        {/* <Route path="/" element={<Home />} /> */}
        <Route path="/" element={<DynamicSignup />} />
      </Routes>
    </>
  )
}

export default App
