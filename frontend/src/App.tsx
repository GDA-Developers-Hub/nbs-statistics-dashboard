import { Routes, Route } from 'react-router-dom'
import { Toaster } from '@/components/ui/toaster'
import { AuthProvider } from '@/contexts/AuthContext'
import ProtectedRoute from '@/components/auth/ProtectedRoute'

// Layouts
import DashboardLayout from '@/components/layouts/DashboardLayout'

// Pages
import Landing from '@/pages/Landing'
import Overview from '@/pages/dashboard/Overview'
import PopulationStatistics from '@/pages/dashboard/PopulationStatistics'
import EconomicIndicators from '@/pages/dashboard/EconomicIndicators'
import SocialDevelopment from '@/pages/dashboard/SocialDevelopment'
import Infrastructure from '@/pages/dashboard/Infrastructure'
import DataExplorer from '@/pages/dashboard/DataExplorer'
import Settings from '@/pages/dashboard/Settings'
import Login from '@/pages/auth/Login'
import NotFound from '@/pages/NotFound'

const App = () => {
  return (
    <AuthProvider>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        
        {/* Dashboard routes - protected */}
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Overview />} />
          <Route path="population" element={<PopulationStatistics />} />
          <Route path="economic" element={<EconomicIndicators />} />
          <Route path="social" element={<SocialDevelopment />} />
          <Route path="infrastructure" element={<Infrastructure />} />
          <Route path="explorer" element={<DataExplorer />} />
          <Route path="settings" element={
            <ProtectedRoute requiredRole="super_admin">
              <Settings />
            </ProtectedRoute>
          } />
        </Route>
        
        {/* Catch all */}
        <Route path="*" element={<NotFound />} />
      </Routes>
      
      <Toaster />
    </AuthProvider>
  )
}

export default App
