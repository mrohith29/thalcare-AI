import { useState } from 'react'
import { useNavigate, Routes, Route } from 'react-router-dom'
import Login from './register/Login'
import Signup from './register/signup'
import './App.css'

function Home() {
  const navigate = useNavigate()

  return (
    <>
      <h2>Welcome to ThalCare AI</h2>
      <button onClick={() => navigate('/login')}>Login</button>
      <br /><br />
      <button onClick={() => navigate('/signup')}>Register</button>
    </>
  )
}

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </>
  )
}

export default App