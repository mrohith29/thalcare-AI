import { useState } from 'react'

export default function SearchFilters({ activeTab, onSearch, onRefresh }) {
  const [filters, setFilters] = useState({})
  const [showFilters, setShowFilters] = useState(false)

  const bloodTypes = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value }
    setFilters(newFilters)
    onSearch(newFilters)
  }

  const clearFilters = () => {
    setFilters({})
    onSearch({})
  }

  const getFilterOptions = () => {
    switch (activeTab) {
      case 'donors':
        return (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Blood Type</label>
              <select
                value={filters.blood_type || ''}
                onChange={(e) => handleFilterChange('blood_type', e.target.value || null)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Blood Types</option>
                {bloodTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Availability</label>
              <select
                value={filters.available !== undefined ? filters.available.toString() : ''}
                onChange={(e) => handleFilterChange('available', e.target.value === '' ? undefined : e.target.value === 'true')}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All</option>
                <option value="true">Available</option>
                <option value="false">Unavailable</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">City</label>
              <input
                type="text"
                placeholder="Enter city"
                value={filters.city || ''}
                onChange={(e) => handleFilterChange('city', e.target.value || null)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">State</label>
              <input
                type="text"
                placeholder="Enter state"
                value={filters.state || ''}
                onChange={(e) => handleFilterChange('state', e.target.value || null)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        )

      case 'patients':
        return (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Blood Type</label>
              <select
                value={filters.blood_type || ''}
                onChange={(e) => handleFilterChange('blood_type', e.target.value || null)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Blood Types</option>
                {bloodTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">City</label>
              <input
                type="text"
                placeholder="Enter city"
                value={filters.city || ''}
                onChange={(e) => handleFilterChange('city', e.target.value || null)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">State</label>
              <input
                type="text"
                placeholder="Enter state"
                value={filters.state || ''}
                onChange={(e) => handleFilterChange('state', e.target.value || null)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Severity Level</label>
              <select
                value={filters.severity_level || ''}
                onChange={(e) => handleFilterChange('severity_level', e.target.value || null)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Levels</option>
                <option value="minor">Minor</option>
                <option value="intermedia">Intermedia</option>
                <option value="major">Major</option>
              </select>
            </div>
          </div>
        )

      case 'hospitals':
        return (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Thalassemia Specialist</label>
              <select
                value={filters.thalassemia_specialist !== undefined ? filters.thalassemia_specialist.toString() : ''}
                onChange={(e) => handleFilterChange('thalassemia_specialist', e.target.value === '' ? undefined : e.target.value === 'true')}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Hospitals</option>
                <option value="true">Specialist Only</option>
                <option value="false">Non-Specialist</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">City</label>
              <input
                type="text"
                placeholder="Enter city"
                value={filters.city || ''}
                onChange={(e) => handleFilterChange('city', e.target.value || null)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">State</label>
              <input
                type="text"
                placeholder="Enter state"
                value={filters.state || ''}
                onChange={(e) => handleFilterChange('state', e.target.value || null)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Rating</label>
              <select
                value={filters.min_rating || ''}
                onChange={(e) => handleFilterChange('min_rating', e.target.value || null)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Any Rating</option>
                <option value="4">4+ Stars</option>
                <option value="3">3+ Stars</option>
                <option value="2">2+ Stars</option>
              </select>
            </div>
          </div>
        )

      case 'doctors':
        return (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Thalassemia Specialist</label>
              <select
                value={filters.thalassemia_specialist !== undefined ? filters.thalassemia_specialist.toString() : ''}
                onChange={(e) => handleFilterChange('thalassemia_specialist', e.target.value === '' ? undefined : e.target.value === 'true')}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Doctors</option>
                <option value="true">Specialist Only</option>
                <option value="false">Non-Specialist</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Availability</label>
              <select
                value={filters.available !== undefined ? filters.available.toString() : ''}
                onChange={(e) => handleFilterChange('available', e.target.value === '' ? undefined : e.target.value === 'true')}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All</option>
                <option value="true">Available</option>
                <option value="false">Unavailable</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">City</label>
              <input
                type="text"
                placeholder="Enter city"
                value={filters.city || ''}
                onChange={(e) => handleFilterChange('city', e.target.value || null)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">State</label>
              <input
                type="text"
                placeholder="Enter state"
                value={filters.state || ''}
                onChange={(e) => handleFilterChange('state', e.target.value || null)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-800">Search Filters</h3>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          >
            <span>{showFilters ? 'Hide' : 'Show'} Filters</span>
            <span className="text-lg">{showFilters ? '−' : '+'}</span>
          </button>
          
          <button
            onClick={onRefresh}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
          >
            <span>🔄</span>
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {showFilters && (
        <div className="space-y-4">
          {getFilterOptions()}
          
          <div className="flex justify-end">
            <button
              onClick={clearFilters}
              className="px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            >
              Clear All Filters
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
