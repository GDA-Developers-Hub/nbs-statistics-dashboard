import { useState } from 'react'
import { Outlet } from 'react-router-dom'
import { Menu, X, BarChart2, Users, TrendingUp, School, Building2, Database, Settings } from 'lucide-react'
import { Link, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'
import GlobalFilters from '@/components/filters/GlobalFilters'

const Sidebar = ({ open, setOpen }: { open: boolean; setOpen: (open: boolean) => void }) => {
  const location = useLocation()
  
  const menuItems = [
    { icon: BarChart2, label: 'Overview', path: '/dashboard' },
    { icon: Users, label: 'Population', path: '/dashboard/population' },
    { icon: TrendingUp, label: 'Economic', path: '/dashboard/economic' },
    { icon: School, label: 'Social', path: '/dashboard/social' },
    { icon: Building2, label: 'Infrastructure', path: '/dashboard/infrastructure' },
    { icon: Database, label: 'Data Explorer', path: '/dashboard/explorer' },
    { icon: Settings, label: 'Settings', path: '/dashboard/settings' },
  ]

  return (
    <div
      className={cn(
        'fixed inset-y-0 left-0 z-50 w-64 transform bg-white shadow-lg transition-transform duration-300 ease-in-out dark:bg-gray-900 md:relative md:translate-x-0',
        open ? 'translate-x-0' : '-translate-x-full'
      )}
    >
      <div className="flex h-16 items-center justify-between px-4">
        <Link to="/" className="flex items-center">
          <span className="text-xl font-bold">SNBS Dashboard</span>
        </Link>
        <button
          onClick={() => setOpen(false)}
          className="p-2 text-gray-500 md:hidden"
        >
          <X size={20} />
        </button>
      </div>
      <nav className="mt-8 px-4">
        <ul className="space-y-2">
          {menuItems.map((item) => {
            const isActive = location.pathname === item.path
            const Icon = item.icon
            
            return (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={cn(
                    'flex items-center rounded-md px-4 py-2 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-primary text-primary-foreground'
                      : 'text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800'
                  )}
                >
                  <Icon className="mr-3 h-5 w-5" />
                  {item.label}
                </Link>
              </li>
            )
          })}
        </ul>
      </nav>
    </div>
  )
}

const DashboardLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} />
      
      <div className="flex flex-1 flex-col overflow-hidden">
        <header className="flex h-16 items-center justify-between border-b px-4">
          <button
            onClick={() => setSidebarOpen(true)}
            className="p-2 text-gray-600 md:hidden"
          >
            <Menu size={20} />
          </button>
          
          <h1 className="text-xl font-semibold md:hidden">Dashboard</h1>
          
          <div className="flex items-center">
            {/* User profile placeholder */}
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-200">
              <span className="text-sm font-medium">U</span>
            </div>
          </div>
        </header>
        
        <div className="flex flex-1 flex-col overflow-auto">
          <div className="border-b p-4">
            <GlobalFilters />
          </div>
          
          <main className="flex-1 p-4 md:p-6">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  )
}

export default DashboardLayout
