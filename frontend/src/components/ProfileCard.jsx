import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8000'

export default function ProfileCard({ profile, userType }) {
  const [specificData, setSpecificData] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchSpecificData()
  }, [profile.id])

  const fetchSpecificData = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/profiles/${profile.id}`, {
        headers: {
          'Content-Type': 'application/json',
        },
      })
      setSpecificData(response.data.specific_data || {})
    } catch (error) {
      console.error('Error fetching specific data:', error)
      if (error.response) {
        console.error('Response data:', error.response.data)
        console.error('Response status:', error.response.status)
      }
    } finally {
      setLoading(false)
    }
  }

  const getStatusBadge = () => {
    if (userType === 'donor') {
      return specificData.available ? (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
          Available
        </span>
      ) : (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
          Unavailable
        </span>
      )
    }
    
    if (userType === 'doctor') {
      return specificData.available ? (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
          Available
        </span>
      ) : (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
          Unavailable
        </span>
      )
    }
    
    if (userType === 'hospital') {
      return specificData.thalassemia_specialist ? (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
          Thalassemia Specialist
        </span>
      ) : null
    }
    
    return null
  }

  const getIcon = () => {
    switch (userType) {
      case 'donor': return '🩸'
      case 'patient': return '👥'
      case 'hospital': return '🏥'
      case 'doctor': return '👨‍⚕️'
      default: return '👤'
    }
  }

  const getCardColor = () => {
    switch (userType) {
      case 'donor': return 'border-red-200 bg-red-50'
      case 'patient': return 'border-blue-200 bg-blue-50'
      case 'hospital': return 'border-green-200 bg-green-50'
      case 'doctor': return 'border-purple-200 bg-purple-50'
      default: return 'border-gray-200 bg-gray-50'
    }
  }

  const getSpecificInfo = () => {
    if (loading) {
      return <div className="animate-pulse bg-gray-200 h-4 rounded w-3/4"></div>
    }

    switch (userType) {
      case 'donor':
        return (
          <div className="space-y-2">
            {specificData.blood_type && (
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-gray-600">Blood Type:</span>
                <span className="text-sm bg-red-100 text-red-800 px-2 py-1 rounded-full font-semibold">
                  {specificData.blood_type}
                </span>
              </div>
            )}
            {specificData.total_donations !== undefined && (
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-gray-600">Total Donations:</span>
                <span className="text-sm font-semibold text-gray-800">{specificData.total_donations}</span>
              </div>
            )}
            {specificData.last_donation_date && (
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-gray-600">Last Donation:</span>
                <span className="text-sm text-gray-800">
                  {new Date(specificData.last_donation_date).toLocaleDateString()}
                </span>
              </div>
            )}
          </div>
        )
      
      case 'patient':
        return (
          <div className="space-y-2">
            {specificData.blood_type && (
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-gray-600">Blood Type:</span>
                <span className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded-full font-semibold">
                  {specificData.blood_type}
                </span>
              </div>
            )}
            {specificData.thalassemia_type && (
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-gray-600">Type:</span>
                <span className="text-sm font-semibold text-gray-800 capitalize">
                  {specificData.thalassemia_type}
                </span>
              </div>
            )}
            {specificData.severity_level && (
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-gray-600">Severity:</span>
                <span className={`text-sm px-2 py-1 rounded-full font-semibold ${
                  specificData.severity_level === 'major' ? 'bg-red-100 text-red-800' :
                  specificData.severity_level === 'intermedia' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-green-100 text-green-800'
                }`}>
                  {specificData.severity_level}
                </span>
              </div>
            )}
          </div>
        )
      
      case 'hospital':
        return (
          <div className="space-y-2">
            {specificData.services && specificData.services.length > 0 && (
              <div className="flex items-start gap-2">
                <span className="text-sm font-medium text-gray-600">Services:</span>
                <div className="flex flex-wrap gap-1">
                  {specificData.services.slice(0, 3).map((service, index) => (
                    <span key={index} className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                      {service}
                    </span>
                  ))}
                  {specificData.services.length > 3 && (
                    <span className="text-xs text-gray-500">+{specificData.services.length - 3} more</span>
                  )}
                </div>
              </div>
            )}
            {specificData.rating !== undefined && (
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-gray-600">Rating:</span>
                <div className="flex items-center gap-1">
                  <span className="text-sm font-semibold text-gray-800">{specificData.rating}</span>
                  <span className="text-yellow-500">⭐</span>
                  <span className="text-xs text-gray-500">({specificData.total_ratings || 0})</span>
                </div>
              </div>
            )}
          </div>
        )
      
      case 'doctor':
        return (
          <div className="space-y-2">
            {specificData.specialization && (
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-gray-600">Specialization:</span>
                <span className="text-sm font-semibold text-gray-800">{specificData.specialization}</span>
              </div>
            )}
            {specificData.experience_years !== undefined && (
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-gray-600">Experience:</span>
                <span className="text-sm font-semibold text-gray-800">{specificData.experience_years} years</span>
              </div>
            )}
            {specificData.consultation_fee !== undefined && (
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-gray-600">Consultation Fee:</span>
                <span className="text-sm font-semibold text-gray-800">₹{specificData.consultation_fee}</span>
              </div>
            )}
          </div>
        )
      
      default:
        return null
    }
  }

  return (
    <div className={`border rounded-xl p-6 hover:shadow-lg transition-all duration-300 ${getCardColor()}`}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="text-3xl">{getIcon()}</div>
          <div>
            <h3 className="font-semibold text-gray-800 text-lg">
              {userType === 'hospital' ? specificData.hospital_name || profile.name : 
               `${profile.first_name || ''} ${profile.last_name || ''}`.trim() || profile.email}
            </h3>
            <p className="text-sm text-gray-600 capitalize">{userType}</p>
          </div>
        </div>
        {getStatusBadge()}
      </div>

      <div className="space-y-3 mb-4">
        {profile.city && (
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <span>📍</span>
            <span>{profile.city}{profile.state && `, ${profile.state}`}</span>
          </div>
        )}
        
        {profile.phone && (
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <span>📞</span>
            <span>{profile.phone}</span>
          </div>
        )}
        
        {profile.email && (
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <span>✉️</span>
            <span className="truncate">{profile.email}</span>
          </div>
        )}
      </div>

      <div className="border-t pt-4">
        {getSpecificInfo()}
      </div>

      <div className="mt-4 flex gap-2">
        <button className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium">
          Contact
        </button>
        <button className="flex-1 bg-gray-100 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-200 transition-colors text-sm font-medium">
          View Details
        </button>
      </div>
    </div>
  )
}
