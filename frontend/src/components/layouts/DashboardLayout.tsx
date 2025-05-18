import { useState } from 'react'
import { Outlet, useNavigate } from 'react-router-dom'
import { Menu, X, BarChart2, Users, TrendingUp, School, Building2, Database, Settings, LogOut, User } from 'lucide-react'
import { Link, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'
import GlobalFilters from '@/components/filters/GlobalFilters'
import { useAuth } from '@/contexts/AuthContext'
import { 
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

const Sidebar = ({ open, setOpen }: { open: boolean; setOpen: (open: boolean) => void }) => {
  const location = useLocation()
  const { user } = useAuth()
  
  // Base menu items available to all users
  const menuItems = [
    { icon: BarChart2, label: 'Overview', path: '/dashboard' },
    { icon: Users, label: 'Population', path: '/dashboard/population' },
    { icon: TrendingUp, label: 'Economic', path: '/dashboard/economic' },
    { icon: School, label: 'Social', path: '/dashboard/social' },
    { icon: Building2, label: 'Infrastructure', path: '/dashboard/infrastructure' },
    { icon: Database, label: 'Data Explorer', path: '/dashboard/explorer' },
  ]
  
  // Add settings only for admin users
  const isAdmin = user?.role === 'super_admin' || user?.role === 'admin'
  if (isAdmin) {
    menuItems.push({ icon: Settings, label: 'Settings', path: '/dashboard/settings' })
  }

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
          aria-label="Close sidebar"
        >
          <X size={20} />
        </button>
      </div>
      <nav className="mt-8 px-4">
        <ul className="space-y-2">
          {menuItems.map((item) => {
            const isActive = 
              item.path === '/dashboard' 
                ? location.pathname === item.path
                : location.pathname.startsWith(item.path);
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

const UserMenu = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  
  const handleLogout = () => {
    logout()
    navigate('/login')
  }
  
  return (
    <DropdownMenu>
      <DropdownMenuTrigger className="flex items-center rounded-full border p-1 hover:bg-gray-100 focus:outline-none">
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground">
          <span className="text-sm font-medium">
            {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
          </span>
        </div>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuLabel>
          <div>
            <p className="font-medium">{user?.full_name || user?.email}</p>
            <p className="text-xs text-gray-500">{user?.role}</p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem className="cursor-pointer" onClick={() => navigate('/profile')}>
          <User className="mr-2 h-4 w-4" />
          Profile
        </DropdownMenuItem>
        <DropdownMenuItem className="cursor-pointer text-red-600" onClick={handleLogout}>
          <LogOut className="mr-2 h-4 w-4" />
          Log out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

const DashboardLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { user } = useAuth()

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} />
      
      <div className="flex flex-1 flex-col overflow-hidden">
        <header className="flex h-16 items-center justify-between border-b px-4">
          <button
            onClick={() => setSidebarOpen(true)}
            className="p-2 text-gray-600 md:hidden"
            aria-label="Open sidebar"
          >
            <Menu size={20} />
          </button>
          
          <h1 className="text-xl font-semibold md:hidden">Dashboard</h1>
          
          <div className="flex items-center">
            <UserMenu />
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
