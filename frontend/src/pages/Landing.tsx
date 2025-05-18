import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { ArrowRight, BarChart2, Map, TrendingUp, ChevronUp, Database, LineChart } from 'lucide-react'
import { cn } from '@/lib/utils'
import SomaliaMap from '@/components/map/SomaliaMap'

const Landing = () => {
  const [scrolled, setScrolled] = useState(false)
  const [visible, setVisible] = useState(Array(4).fill(false))
  
  // Handle scroll effects
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50)
      
      // Check if sections are in view for animations
      const sections = document.querySelectorAll('.animate-on-scroll')
      sections.forEach((section, index) => {
        const rect = section.getBoundingClientRect()
        const isVisible = rect.top <= window.innerHeight * 0.75
        if (isVisible) {
          setVisible(prev => {
            const newState = [...prev]
            newState[index] = true
            return newState
          })
        }
      })
    }
    
    // Initialize scroll listener
    window.addEventListener('scroll', handleScroll)
    
    // Trigger initial animations
    setTimeout(() => {
      setVisible([true, false, false, false])
    }, 300)
    
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])
  
  // Scroll to top function
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
  
  // Mock data for statistical highlights
  const keyStats = [
    { label: 'Population', value: '16.3M', change: '+2.9%', trend: 'up' },
    { label: 'GDP Growth', value: '4.2%', change: '+0.5%', trend: 'up' },
    { label: 'Literacy Rate', value: '40%', change: '+5%', trend: 'up' },
    { label: 'Inflation', value: '6.1%', change: '-0.8%', trend: 'down' },
  ]

  return (
    <div className="flex min-h-screen flex-col">
      {/* Header - with background blur effect on scroll */}
      <header className={cn(
        "fixed top-0 w-full z-50 transition-all duration-300",
        scrolled 
          ? "bg-white/80 backdrop-blur-md shadow-sm" 
          : "bg-transparent"
      )}>
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className="h-8 w-8 rounded-md bg-blue-600 flex items-center justify-center">
                <Database className="h-4 w-4 text-white" />
              </div>
              <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-cyan-500">
                SNBS Dashboard
              </span>
            </Link>
          </div>
          <nav className="hidden space-x-6 md:flex">
            <Link to="/" className="text-sm font-medium hover:text-blue-600 transition-colors">Home</Link>
            <Link to="/dashboard" className="text-sm font-medium hover:text-blue-600 transition-colors">Dashboard</Link>
            <a href="#about" className="text-sm font-medium hover:text-blue-600 transition-colors">About</a>
          </nav>
          <div>
            <Link to="/login">
              <Button variant="outline" size="sm" className="mr-2 hover:bg-blue-50 transition-colors">
                Log In
              </Button>
            </Link>
          </div>
        </div>
      </header>
      
      {/* Empty space to offset fixed header */}
      <div className="h-16"></div>

      {/* Hero Section - with animated entrance */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-50 via-sky-50 to-white py-24">
        {/* Abstract background pattern */}
        <div className="absolute inset-0 z-0 opacity-20">
          <div className="absolute top-10 left-10 h-64 w-64 rounded-full bg-blue-300 blur-3xl"></div>
          <div className="absolute bottom-10 right-10 h-64 w-64 rounded-full bg-cyan-300 blur-3xl"></div>
        </div>
        
        <div className="container relative z-10 mx-auto px-4 text-center">
          <div className={cn(
            "transform transition-all duration-700",
            visible[0] ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
          )}>
            <h1 className="mb-6 text-4xl font-extrabold md:text-6xl">
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-cyan-500">
                Somalia National Bureau of Statistics
              </span>
            </h1>
            <p className="mx-auto mb-8 max-w-3xl text-lg text-gray-600 leading-relaxed">
              Explore official statistical data and indicators for Somalia through our interactive dashboard. 
              Access demographic, economic, and social development metrics to gain insights into Somalia's progress.
            </p>
            <Link to="/dashboard">
              <Button size="lg" className="px-8 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 transition-all duration-300 shadow-md hover:shadow-lg">
                Explore Dashboard <ArrowRight className="ml-2 h-4 w-4 animate-pulse" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Statistical Highlights - with animation */}
      <section className="py-16 animate-on-scroll">
        <div className="container mx-auto px-4">
          <div className={cn(
            "transform transition-all duration-700 delay-100",
            visible[1] ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
          )}>
            <h2 className="mb-8 text-center text-3xl font-bold">
              <span className="relative inline-block">
                <span className="relative z-10">Statistical Highlights</span>
                <span className="absolute bottom-0 left-0 h-3 w-full bg-blue-100 z-0"></span>
              </span>
            </h2>
            
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
              {keyStats.map((stat, index) => (
                <div
                  key={index}
                  className="rounded-lg bg-white p-6 shadow-md transition-all duration-300 hover:shadow-xl hover:translate-y-[-5px] border-t-4 border-blue-500 group"
                >
                  <h3 className="mb-2 text-sm font-medium text-gray-500 group-hover:text-blue-600 transition-colors">{stat.label}</h3>
                  <div className="flex items-baseline">
                    <span className="text-3xl font-bold group-hover:text-blue-700 transition-colors">{stat.value}</span>
                    <span className={`ml-2 text-sm font-medium flex items-center ${
                      stat.trend === 'up' ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {stat.change}
                      {stat.trend === 'up' ? (
                        <ArrowRight className="h-3 w-3 ml-1 rotate-45" />
                      ) : (
                        <ArrowRight className="h-3 w-3 ml-1 rotate-[135deg]" />
                      )}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features Section - with animated cards */}
      <section className="bg-gradient-to-b from-white to-blue-50 py-20 animate-on-scroll">
        <div className="container mx-auto px-4">
          <div className={cn(
            "transform transition-all duration-700 delay-200",
            visible[2] ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
          )}>
            <h2 className="mb-12 text-center text-3xl font-bold">
              <span className="relative inline-block">
                <span className="relative z-10">Dashboard Features</span>
                <span className="absolute bottom-0 left-0 h-3 w-full bg-blue-100 z-0"></span>
              </span>
            </h2>
            <div className="grid gap-8 md:grid-cols-3">
              <div className="flex flex-col items-center text-center rounded-xl bg-white p-8 shadow-lg transition-all duration-300 hover:shadow-xl hover:translate-y-[-5px] border border-gray-100">
                <div className="mb-6 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 p-4 transform transition-transform group-hover:scale-110">
                  <BarChart2 className="h-8 w-8 text-white" />
                </div>
                <h3 className="mb-3 text-xl font-semibold text-gray-800">Interactive Charts</h3>
                <p className="text-gray-600 leading-relaxed">
                  Visualize key indicators with interactive charts that allow you to track trends over time and gain valuable insights.
                </p>
              </div>
              <div className="flex flex-col items-center text-center rounded-xl bg-white p-8 shadow-lg transition-all duration-300 hover:shadow-xl hover:translate-y-[-5px] border border-gray-100">
                <div className="mb-6 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 p-4">
                  <Map className="h-8 w-8 text-white" />
                </div>
                <h3 className="mb-3 text-xl font-semibold text-gray-800">Regional GIS Map</h3>
                <p className="text-gray-600 leading-relaxed">
                  Explore data with our interactive map of Somalia. Filter statistics by region to understand local trends and patterns.
                </p>
              </div>
              <div className="flex flex-col items-center text-center rounded-xl bg-white p-8 shadow-lg transition-all duration-300 hover:shadow-xl hover:translate-y-[-5px] border border-gray-100">
                <div className="mb-6 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 p-4">
                  <TrendingUp className="h-8 w-8 text-white" />
                </div>
                <h3 className="mb-3 text-xl font-semibold text-gray-800">Data Explorer</h3>
                <p className="text-gray-600 leading-relaxed">
                  Create custom views with our data explorer tool. Compare indicators across sectors and time periods for comprehensive analysis.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Interactive Map Placeholder - with enhanced styling */}
      <section className="py-20 animate-on-scroll">
        <div className="container mx-auto px-4">
          <div className={cn(
            "transform transition-all duration-700 delay-300",
            visible[3] ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
          )}>
            <div className="mb-8 flex flex-col items-center">
              <h2 className="mb-4 text-3xl font-bold">
                <span className="relative inline-block">
                  <span className="relative z-10">Interactive Map</span>
                  <span className="absolute bottom-0 left-0 h-3 w-full bg-blue-100 z-0"></span>
                </span>
              </h2>
              <p className="mb-6 max-w-2xl text-center text-gray-600 leading-relaxed">
                Click on a region to view detailed statistics for that area and explore Somalia's geographical data.
              </p>
            </div>
            <div className="mx-auto aspect-video max-w-4xl rounded-xl overflow-hidden shadow-xl border border-gray-200">
              {/* Real Somalia Map component with Mapbox integration */}
              <SomaliaMap 
                selectedRegion="all" 
                onRegionSelect={(regionCode) => {
                  console.log('Selected region:', regionCode);
                  // This is just for demonstration in the landing page
                  // We don't actually change the region selection here
                }}
                height="500px"
              />
            </div>
            <div className="mt-8 flex justify-center">
              <Link to="/dashboard">
                <Button variant="outline" className="rounded-full px-8 py-6 font-medium hover:bg-blue-50 transition-all duration-300 flex items-center space-x-2 border-blue-200 shadow-sm hover:shadow-md">
                  <span>Open Full Map in Dashboard</span>
                  <ArrowRight className="h-4 w-4 ml-2" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Recent Updates - with enhanced styling */}
      <section className="bg-gradient-to-b from-blue-50 to-white py-20 animate-on-scroll">
        <div className="container mx-auto px-4">
          <div className={cn(
            "transform transition-all duration-700 delay-400",
            visible[3] ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
          )}>
            <h2 className="mb-10 text-center text-3xl font-bold">
              <span className="relative inline-block">
                <span className="relative z-10">Latest Updates</span>
                <span className="absolute bottom-0 left-0 h-3 w-full bg-blue-100 z-0"></span>
              </span>
            </h2>
            <div className="mx-auto max-w-3xl space-y-4">
              {[
                { title: 'Census Population Data Updated', date: 'May 15, 2025', tag: 'Demographics' },
                { title: 'Q1 2025 Economic Indicators Released', date: 'April 28, 2025', tag: 'Economics' },
                { title: 'Annual Education Statistics Report', date: 'March 10, 2025', tag: 'Education' },
                { title: 'Regional Development Indices', date: 'February 22, 2025', tag: 'Development' },
              ].map((update, index) => (
                <div 
                  key={index} 
                  className="rounded-xl border border-gray-100 bg-white p-4 shadow-md hover:shadow-lg transition-all duration-300 hover:translate-x-1"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
                    <div className="flex items-center">
                      <div className="mr-3 rounded-md bg-blue-100 px-2 py-1 text-xs font-medium text-blue-700">{update.tag}</div>
                      <h3 className="font-medium">{update.title}</h3>
                    </div>
                    <span className="mt-2 sm:mt-0 text-sm text-gray-500 flex items-center">
                      <LineChart className="h-3 w-3 mr-1" />
                      {update.date}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Footer - with enhanced styling */}
      <footer className="mt-auto bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="h-8 w-8 rounded-md bg-blue-600 flex items-center justify-center">
                  <Database className="h-4 w-4 text-white" />
                </div>
                <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-300">
                  SNBS Dashboard
                </span>
              </div>
              <p className="text-gray-400 mb-4">
                Somalia's official statistical data platform providing access to demographic, economic, and development indicators.              
              </p>
              <span className="text-sm text-gray-500">
                © 2025 Somalia National Bureau of Statistics
              </span>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
              <ul className="space-y-2">
                <li><Link to="/dashboard" className="text-gray-400 hover:text-white transition-colors">Dashboard</Link></li>
                <li><Link to="/dashboard/population" className="text-gray-400 hover:text-white transition-colors">Population Statistics</Link></li>
                <li><Link to="/dashboard/economic" className="text-gray-400 hover:text-white transition-colors">Economic Indicators</Link></li>
                <li><Link to="/dashboard/social" className="text-gray-400 hover:text-white transition-colors">Social Development</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Legal</h3>
              <ul className="space-y-2">
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Terms of Service</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Contact</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Data Usage Guidelines</a></li>
              </ul>
            </div>
          </div>
        </div>
      </footer>
      
      {/* Scroll to top button */}
      <button 
        onClick={scrollToTop}
        className={cn(
          "fixed bottom-6 right-6 h-12 w-12 rounded-full bg-blue-600 text-white shadow-lg flex items-center justify-center transition-all duration-300 hover:bg-blue-700 focus:outline-none z-50",
          scrolled ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10 pointer-events-none"
        )}
      >
        <ChevronUp className="h-6 w-6" />
      </button>
    </div>
  )
}

export default Landing
