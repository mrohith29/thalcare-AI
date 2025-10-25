import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import ProfileCard from './ProfileCard'
import SearchFilters from './SearchFilters'
import StatsCard from './StatsCard'

const API_BASE_URL = 'http://127.0.0.1:8000'

export default function Dashboard({ user, setIsAuthenticated }) {
  const [activeTab, setActiveTab] = useState('donors')
  const [profiles, setProfiles] = useState([])
  const [filteredProfiles, setFilteredProfiles] = useState([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({})
  const [searchFilters, setSearchFilters] = useState({})
  const navigate = useNavigate()

  const tabs = [
    { id: 'donors', label: 'Find Donors', icon: '🩸', color: 'red' },
    { id: 'patients', label: 'Search Patients', icon: '👥', color: 'blue' },
    { id: 'hospitals', label: 'Hospitals', icon: '🏥', color: 'green' },
    { id: 'doctors', label: 'Doctors', icon: '👨‍⚕️', color: 'purple' }
  ]

  useEffect(() => {
    fetchStats()
    fetchProfiles()
  }, [])

  useEffect(() => {
    filterProfiles()
  }, [profiles, searchFilters])

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/stats`)
      setStats(response.data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  const fetchProfiles = async () => {
    setLoading(true)
    try {
      const response = await axios.get(`${API_BASE_URL}/profiles`)
      setProfiles(response.data.profiles || [])
    } catch (error) {
      console.error('Error fetching profiles:', error)
    } finally {
      setLoading(false)
    }
  }

  const filterProfiles = () => {
    let filtered = profiles.filter(profile => {
      // Filter by user type based on active tab
      if (activeTab === 'donors' && profile.user_type !== 'donor') return false
      if (activeTab === 'patients' && profile.user_type !== 'patient') return false
      if (activeTab === 'hospitals' && profile.user_type !== 'hospital') return false
      if (activeTab === 'doctors' && profile.user_type !== 'doctor') return false

      // Apply search filters
      if (searchFilters.city && !profile.city?.toLowerCase().includes(searchFilters.city.toLowerCase())) return false
      if (searchFilters.state && !profile.state?.toLowerCase().includes(searchFilters.state.toLowerCase())) return false
      if (searchFilters.blood_type && profile.blood_type !== searchFilters.blood_type) return false
      if (searchFilters.thalassemia_specialist !== undefined && profile.thalassemia_specialist !== searchFilters.thalassemia_specialist) return false
      if (searchFilters.available !== undefined && profile.available !== searchFilters.available) return false

      return true
    })

    setFilteredProfiles(filtered)
  }

  const handleSearch = (filters) => {
    setSearchFilters(filters)
  }

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    setIsAuthenticated(false)
    navigate('/')
  }

  const getTabColor = (tabId) => {
    const tab = tabs.find(t => t.id === tabId)
    const colors = {
      red: 'border-red-500 text-red-600 bg-red-50',
      blue: 'border-blue-500 text-blue-600 bg-blue-50',
      green: 'border-green-500 text-green-600 bg-green-50',
      purple: 'border-purple-500 text-purple-600 bg-purple-50'
    }
    return colors[tab?.color] || 'border-gray-300 text-gray-600'
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                ThalCare AI
              </h1>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="text-sm text-gray-600">
                Welcome, {user?.first_name || user?.email}
              </div>
              <button
                onClick={handleLogout}
                className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <StatsCard 
            title="Total Donors" 
            value={stats.donor_count || 0} 
            icon="🩸" 
            color="red"
          />
          <StatsCard 
            title="Total Patients" 
            value={stats.patient_count || 0} 
            icon="👥" 
            color="blue"
          />
          <StatsCard 
            title="Total Hospitals" 
            value={stats.hospital_count || 0} 
            icon="🏥" 
            color="green"
          />
          <StatsCard 
            title="Total Doctors" 
            value={stats.doctor_count || 0} 
            icon="👨‍⚕️" 
            color="purple"
          />
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-xl shadow-sm border mb-8">
          <div className="flex flex-wrap border-b">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-6 py-4 border-b-2 font-medium transition-all duration-200 ${
                  activeTab === tab.id
                    ? getTabColor(tab.id)
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }`}
              >
                <span className="text-xl">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Search Filters */}
        <div className="bg-white rounded-xl shadow-sm border mb-8">
          <SearchFilters 
            activeTab={activeTab}
            onSearch={handleSearch}
            onRefresh={fetchProfiles}
          />
        </div>

        {/* Results */}
        <div className="bg-white rounded-xl shadow-sm border p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-800">
              {tabs.find(t => t.id === activeTab)?.label} ({filteredProfiles.length})
            </h2>
            {loading && (
              <div className="flex items-center gap-2 text-gray-500">
                <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                Loading...
              </div>
            )}
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <div key={i} className="bg-gray-100 rounded-xl h-64 animate-pulse"></div>
              ))}
            </div>
          ) : filteredProfiles.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">🔍</div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">No {activeTab} found</h3>
              <p className="text-gray-600">Try adjusting your search filters</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredProfiles.map((profile) => (
                <ProfileCard 
                  key={profile.id} 
                  profile={profile} 
                  userType={activeTab.slice(0, -1)} // Remove 's' from end
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
