import React from 'react'
import { useAuth } from '@/contexts/AuthContext'

const Dashboard = () => {
  const { user } = useAuth()
  
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      
      {user && (
        <div className="bg-white rounded-lg shadow p-4 mb-6">
          <h2 className="font-medium text-lg mb-2">Welcome, {user.full_name || user.email}</h2>
          <p className="text-gray-500">Role: {user.role}</p>
        </div>
      )}
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="font-medium mb-2">Population Growth</h3>
          <p className="text-gray-500">View population statistics</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="font-medium mb-2">Literacy Rate</h3>
          <p className="text-gray-500">View literacy statistics</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="font-medium mb-2">Vaccination Coverage</h3>
          <p className="text-gray-500">View health statistics</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="font-medium mb-2">CPI Trends</h3>
          <p className="text-gray-500">View economic indicators</p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard 