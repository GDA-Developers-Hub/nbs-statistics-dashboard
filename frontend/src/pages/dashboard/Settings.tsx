import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { toast } from '@/components/ui/use-toast'

const Settings = () => {
  const [user, setUser] = useState({
    email: '',
    role: '',
    name: '',
    organization: '',
    language: 'english',
    darkMode: false,
    notifications: true,
    dataRefreshInterval: '30'
  })

  // Load user data from localStorage on component mount
  useEffect(() => {
    const email = localStorage.getItem('userEmail') || ''
    const role = localStorage.getItem('userRole') || 'Public User'
    
    setUser(prev => ({
      ...prev,
      email,
      role,
      name: email ? email.split('@')[0] : 'Guest User',
      organization: email?.includes('snbs.gov.so') ? 'Somalia National Bureau of Statistics' : 'Guest'
    }))
  }, [])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target
    const isCheckbox = type === 'checkbox'
    const updatedValue = isCheckbox ? (e.target as HTMLInputElement).checked : value
    
    setUser(prev => ({ ...prev, [name]: updatedValue }))
  }
  
  const handleSaveSettings = (e: React.FormEvent) => {
    e.preventDefault()
    
    // In a real app, this would save settings to the backend
    // For demo, we'll just save to localStorage
    localStorage.setItem('userSettings', JSON.stringify(user))
    
    toast({
      title: 'Settings Saved',
      description: 'Your preferences have been updated successfully.'
    })
  }
  
  const handleLogout = () => {
    // Clear authentication data
    localStorage.removeItem('isAuthenticated')
    localStorage.removeItem('userRole')
    localStorage.removeItem('userEmail')
    
    // Redirect to login page (in a real app this would use a router)
    window.location.href = '/login'
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Settings</h1>
      
      <div className="grid gap-6 md:grid-cols-2">
        {/* Profile Settings */}
        <Card>
          <CardHeader>
            <CardTitle>Profile Settings</CardTitle>
            <CardDescription>Manage your account information</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSaveSettings} className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium" htmlFor="email">
                  Email Address
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  value={user.email}
                  onChange={handleChange}
                  readOnly
                  className="w-full rounded-md border border-gray-300 bg-gray-100 px-3 py-2 text-sm"
                />
                <p className="text-xs text-gray-500">Email cannot be changed</p>
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-medium" htmlFor="role">
                  User Role
                </label>
                <input
                  id="role"
                  name="role"
                  type="text"
                  value={user.role}
                  readOnly
                  className="w-full rounded-md border border-gray-300 bg-gray-100 px-3 py-2 text-sm"
                />
                <p className="text-xs text-gray-500">Role is assigned by administrators</p>
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-medium" htmlFor="name">
                  Display Name
                </label>
                <input
                  id="name"
                  name="name"
                  type="text"
                  value={user.name}
                  onChange={handleChange}
                  className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
                />
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-medium" htmlFor="organization">
                  Organization
                </label>
                <input
                  id="organization"
                  name="organization"
                  type="text"
                  value={user.organization}
                  onChange={handleChange}
                  className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
                />
              </div>
              
              <Button type="submit" className="w-full">
                Save Profile Settings
              </Button>
            </form>
          </CardContent>
        </Card>
        
        {/* Application Settings */}
        <Card>
          <CardHeader>
            <CardTitle>Application Settings</CardTitle>
            <CardDescription>Customize your dashboard experience</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSaveSettings} className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium" htmlFor="language">
                  Language
                </label>
                <select
                  id="language"
                  name="language"
                  value={user.language}
                  onChange={handleChange}
                  className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
                >
                  <option value="english">English</option>
                  <option value="somali">Somali</option>
                  <option value="arabic">Arabic</option>
                </select>
              </div>
              
              <div className="flex items-center space-x-2">
                <input
                  id="darkMode"
                  name="darkMode"
                  type="checkbox"
                  checked={user.darkMode}
                  onChange={handleChange}
                  className="h-4 w-4 rounded border-gray-300 text-blue-600"
                />
                <label className="text-sm font-medium" htmlFor="darkMode">
                  Dark Mode
                </label>
              </div>
              
              <div className="flex items-center space-x-2">
                <input
                  id="notifications"
                  name="notifications"
                  type="checkbox"
                  checked={user.notifications}
                  onChange={handleChange}
                  className="h-4 w-4 rounded border-gray-300 text-blue-600"
                />
                <label className="text-sm font-medium" htmlFor="notifications">
                  Enable Notifications
                </label>
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-medium" htmlFor="dataRefreshInterval">
                  Data Refresh Interval
                </label>
                <select
                  id="dataRefreshInterval"
                  name="dataRefreshInterval"
                  value={user.dataRefreshInterval}
                  onChange={handleChange}
                  className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
                >
                  <option value="0">Manual Refresh Only</option>
                  <option value="15">Every 15 minutes</option>
                  <option value="30">Every 30 minutes</option>
                  <option value="60">Every hour</option>
                </select>
              </div>
              
              <Button type="submit" className="w-full">
                Save Application Settings
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
      
      {/* Security Settings */}
      <Card>
        <CardHeader>
          <CardTitle>Security</CardTitle>
          <CardDescription>Manage your account security</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-base font-medium">Password</h3>
              <p className="text-sm text-gray-500">Change your account password</p>
            </div>
            <Button variant="outline">Change Password</Button>
          </div>
          
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-base font-medium">Two-Factor Authentication</h3>
              <p className="text-sm text-gray-500">Add an extra layer of security to your account</p>
            </div>
            <Button variant="outline">Setup 2FA</Button>
          </div>
          
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-base font-medium">Session Management</h3>
              <p className="text-sm text-gray-500">Manage active sessions across devices</p>
            </div>
            <Button variant="outline">View Sessions</Button>
          </div>
          
          <div className="pt-4 border-t border-gray-200">
            <Button variant="destructive" onClick={handleLogout} className="w-full">
              Log Out
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Settings
