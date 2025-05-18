import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { ArrowRight, BarChart2, Map, TrendingUp, ChevronUp, Database } from 'lucide-react'
import { LineChart as LucideLineChart } from 'lucide-react'
import { cn } from '@/lib/utils'
import SomaliaMap from '@/components/map/SomaliaMap'
import { motion } from 'framer-motion'
import { LineChart as RechartsLineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const Landing = () => {
  const [scrolled, setScrolled] = useState(false)
  const [visible, setVisible] = useState(Array(6).fill(false))
  const [liveData, setLiveData] = useState([
    { time: '00:00', value: 65 },
    { time: '02:00', value: 59 },
    { time: '04:00', value: 80 },
    { time: '06:00', value: 81 },
    { time: '08:00', value: 56 },
    { time: '10:00', value: 72 },
    { time: '12:00', value: 89 },
    { time: '14:00', value: 96 },
    { time: '16:00', value: 67 },
    { time: '18:00', value: 75 },
    { time: '20:00', value: 80 },
    { time: '22:00', value: 92 },
    { time: 'now', value: 87 },
  ])
  
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
      setVisible([true, false, false, false, false, false])
    }, 300)
    
    // Simulate live data updates
    const dataInterval = setInterval(() => {
      setLiveData(prevData => {
        // Shift all values left
        const newData = [...prevData];
        
        // Remove first element
        newData.shift();
        
        // Generate a random value between 55-98
        const randomValue = Math.floor(Math.random() * 43) + 55;
        
        // Add new data point at the end
        newData.push({ time: 'now', value: randomValue });
        
        // Update timestamps
        return newData.map((point, index) => {
          if (index === newData.length - 1) return { time: 'now', value: point.value };
          return { time: point.time, value: point.value };
        });
      });
    }, 5000); // Update every 5 seconds
    
    // Clean up event listeners and intervals
    return () => {
      window.removeEventListener('scroll', handleScroll);
      clearInterval(dataInterval);
    }
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
  
  // Data for animated charts
  const populationTrendData = [
    { year: '2018', population: 14.7 },
    { year: '2019', population: 15.1 },
    { year: '2020', population: 15.4 },
    { year: '2021', population: 15.7 },
    { year: '2022', population: 16.0 },
    { year: '2023', population: 16.3 },
  ]
  
  const gdpData = [
    { year: '2018', gdp: 7.3 },
    { year: '2019', gdp: 7.5 },
    { year: '2020', gdp: 7.2 }, // Covid impact
    { year: '2021', gdp: 7.6 },
    { year: '2022', gdp: 7.9 },
    { year: '2023', gdp: 8.2 },
  ]
  
  const sectorContributionData = [
    { name: 'Agriculture', value: 60 },
    { name: 'Services', value: 30 },
    { name: 'Industry', value: 10 },
  ]
  
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28'];

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
        <motion.div 
          className="absolute inset-0 z-0 opacity-30"
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.3 }}
          transition={{ duration: 1.5 }}
        >
          <motion.div 
            className="absolute top-10 left-10 h-64 w-64 rounded-full bg-blue-300 blur-3xl"
            animate={{ 
              scale: [1, 1.2, 1],
              x: [0, 20, 0],
              y: [0, 15, 0],
            }}
            transition={{ 
              duration: 8,
              repeat: Infinity,
              repeatType: "reverse"
            }}
          />
          <motion.div 
            className="absolute bottom-10 right-10 h-64 w-64 rounded-full bg-cyan-300 blur-3xl"
            animate={{ 
              scale: [1, 1.3, 1],
              x: [0, -20, 0],
              y: [0, -15, 0],
            }}
            transition={{ 
              duration: 10,
              repeat: Infinity,
              repeatType: "reverse"
            }}
          />
          <motion.div 
            className="absolute top-1/2 left-1/3 h-48 w-48 rounded-full bg-indigo-200 blur-3xl"
            animate={{ 
              scale: [1, 1.5, 1],
              opacity: [0.3, 0.6, 0.3],
            }}
            transition={{ 
              duration: 12,
              repeat: Infinity,
              repeatType: "reverse"
            }}
          />
        </motion.div>
        
        {/* Data Piping Animation */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          {/* Horizontal data pipelines */}
          <motion.div className="absolute top-1/4 left-0 h-1 bg-gradient-to-r from-blue-500 to-cyan-400 opacity-60"
            initial={{ width: 0 }}
            animate={{ width: '100%' }}
            transition={{ duration: 5, repeat: Infinity, repeatType: "loop" }}
          />
          <motion.div className="absolute top-2/3 right-0 h-1 bg-gradient-to-l from-blue-500 to-cyan-400 opacity-40"
            initial={{ width: 0 }}
            animate={{ width: '100%' }}
            transition={{ duration: 8, repeat: Infinity, repeatType: "loop", delay: 2 }}
          />
          
          {/* Data packets moving across the pipelines */}
          <motion.div 
            className="absolute top-1/4 left-0 h-2 w-6 bg-blue-600 rounded-full shadow-lg shadow-blue-400/50"
            initial={{ x: '-100%' }}
            animate={{ x: '100vw' }}
            transition={{ duration: 5, repeat: Infinity, repeatType: "loop", ease: "linear" }}
          />
          <motion.div 
            className="absolute top-1/4 left-0 h-2 w-4 bg-cyan-500 rounded-full shadow-lg shadow-cyan-400/50"
            initial={{ x: '-100%' }}
            animate={{ x: '100vw' }}
            transition={{ duration: 5, repeat: Infinity, repeatType: "loop", ease: "linear", delay: 1 }}
          />
          <motion.div 
            className="absolute top-1/4 left-0 h-2 w-8 bg-indigo-500 rounded-full shadow-lg shadow-indigo-400/50"
            initial={{ x: '-100%' }}
            animate={{ x: '100vw' }}
            transition={{ duration: 5, repeat: Infinity, repeatType: "loop", ease: "linear", delay: 2.5 }}
          />
          
          <motion.div 
            className="absolute top-2/3 right-0 h-2 w-7 bg-blue-600 rounded-full shadow-lg shadow-blue-400/50"
            initial={{ x: '100vw' }}
            animate={{ x: '-10%' }}
            transition={{ duration: 8, repeat: Infinity, repeatType: "loop", ease: "linear", delay: 2 }}
          />
          <motion.div 
            className="absolute top-2/3 right-0 h-2 w-3 bg-cyan-500 rounded-full shadow-lg shadow-cyan-400/50"
            initial={{ x: '100vw' }}
            animate={{ x: '-10%' }}
            transition={{ duration: 8, repeat: Infinity, repeatType: "loop", ease: "linear", delay: 3.5 }}
          />
          
          {/* Vertical data connections */}
          <div className="absolute left-1/4 top-1/4 h-[calc(100%-40%)] w-1 overflow-hidden">
            <motion.div 
              className="w-full h-1/2 bg-gradient-to-b from-blue-500 to-transparent"
              initial={{ y: '-100%' }}
              animate={{ y: '100%' }}
              transition={{ duration: 3, repeat: Infinity, repeatType: "loop", delay: 1, ease: "easeIn" }}
            />
          </div>
          
          <div className="absolute right-1/3 top-0 h-1/4 w-1 overflow-hidden">
            <motion.div 
              className="w-full h-4 bg-cyan-500 rounded-full"
              initial={{ y: '-100%' }}
              animate={{ y: '400%' }}
              transition={{ duration: 2, repeat: Infinity, repeatType: "loop", delay: 0.5, ease: "easeIn" }}
            />
          </div>
          
          {/* Binary data visualization (1s and 0s) */}
          <motion.div
            className="absolute top-20 right-1/4 text-xs text-blue-500/30 font-mono"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 1, 0] }}
            transition={{ duration: 2, repeat: Infinity, repeatType: "loop", delay: 1 }}
          >
            10110101
          </motion.div>
          <motion.div
            className="absolute bottom-40 left-1/3 text-xs text-cyan-500/30 font-mono"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 1, 0] }}
            transition={{ duration: 2, repeat: Infinity, repeatType: "loop", delay: 1.5 }}
          >
            01001101
          </motion.div>
          <motion.div
            className="absolute top-1/2 right-1/5 text-xs text-indigo-500/30 font-mono"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 1, 0] }}
            transition={{ duration: 2, repeat: Infinity, repeatType: "loop", delay: 2 }}
          >
            11100011
          </motion.div>
        </div>
        
        <div className="container relative z-10 mx-auto px-4 text-center">
          <motion.div 
            className="transform"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
          >
            <motion.h1 
              className="mb-6 text-4xl font-extrabold md:text-6xl"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-cyan-500">
                Somalia National Bureau of Statistics
              </span>
            </motion.h1>
            <motion.p 
              className="mx-auto mb-8 max-w-3xl text-lg text-gray-600 leading-relaxed"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              Explore official statistical data and indicators for Somalia through our interactive dashboard. 
              Access demographic, economic, and social development metrics to gain insights into Somalia's progress.
            </motion.p>
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.7 }}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
            >
              <Link to="/dashboard">
                <Button size="lg" className="px-8 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 transition-all duration-300 shadow-md hover:shadow-lg">
                  <span>Explore Dashboard</span>
                  <motion.div
                    className="inline-block ml-2"
                    animate={{ 
                      x: [0, 5, 0],
                    }}
                    transition={{ 
                      duration: 1.5,
                      repeat: Infinity,
                      repeatType: "reverse"
                    }}
                  >
                    <ArrowRight className="h-4 w-4" />
                  </motion.div>
                </Button>
              </Link>
            </motion.div>
          </motion.div>
          
          {/* Floating data points */}
          <motion.div
            className="absolute -right-16 top-1/4 h-24 w-24 rounded-xl bg-white/90 p-4 shadow-lg flex flex-col items-center justify-center backdrop-blur-sm border border-blue-100"
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7, delay: 1.2 }}
          >
            <span className="text-2xl font-bold text-blue-600">16.3M</span>
            <span className="text-xs text-gray-500">Population</span>
          </motion.div>
          <motion.div
            className="absolute -left-10 top-2/3 h-20 w-28 rounded-xl bg-white/90 p-3 shadow-lg flex flex-col items-center justify-center backdrop-blur-sm border border-green-100 hidden md:flex"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.7, delay: 1.4 }}
          >
            <span className="text-xl font-bold text-green-600">+4.2%</span>
            <span className="text-xs text-gray-500">GDP Growth</span>
          </motion.div>
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
                <motion.div
                  key={index}
                  className="rounded-lg bg-white p-6 shadow-md transition-all duration-300 hover:shadow-xl hover:translate-y-[-5px] border-t-4 border-blue-500 group overflow-hidden relative"
                  initial={{ opacity: 0, y: 20 }}
                  animate={visible[1] ? { opacity: 1, y: 0 } : {}}
                  transition={{ duration: 0.4, delay: 0.1 * index }}
                  whileHover={{ scale: 1.02 }}
                >
                  {/* Animated background gradient */}
                  <motion.div 
                    className="absolute inset-0 bg-gradient-to-r from-blue-50 to-indigo-50 opacity-0 group-hover:opacity-100 transition-opacity"
                    initial={{ x: '-100%' }}
                    animate={visible[1] ? { x: 0 } : {}}
                    transition={{ duration: 1, delay: 0.3 + (0.1 * index) }}
                  />
                  
                  <h3 className="mb-2 text-sm font-medium text-gray-500 group-hover:text-blue-600 transition-colors relative z-10">{stat.label}</h3>
                  <div className="flex items-baseline relative z-10">
                    <motion.span 
                      className="text-3xl font-bold group-hover:text-blue-700 transition-colors"
                      initial={{ opacity: 0 }}
                      animate={visible[1] ? { opacity: 1 } : {}}
                      transition={{ duration: 0.6, delay: 0.3 + (0.15 * index) }}
                    >
                      {stat.value}
                    </motion.span>
                    <motion.span 
                      className={`ml-2 text-sm font-medium flex items-center ${
                        stat.trend === 'up' ? 'text-green-600' : 'text-red-600'
                      }`}
                      initial={{ opacity: 0, x: -10 }}
                      animate={visible[1] ? { opacity: 1, x: 0 } : {}}
                      transition={{ duration: 0.4, delay: 0.5 + (0.1 * index) }}
                    >
                      {stat.change}
                      {stat.trend === 'up' ? (
                        <ArrowRight className="h-3 w-3 ml-1 rotate-45" />
                      ) : (
                        <ArrowRight className="h-3 w-3 ml-1 rotate-[135deg]" />
                      )}
                    </motion.span>
                  </div>
                  <motion.div 
                    className="h-1 bg-blue-200 mt-4 rounded-full overflow-hidden"
                    initial={{ width: 0 }}
                    animate={visible[1] ? { width: '100%' } : {}}
                    transition={{ duration: 1, delay: 0.5 + (0.1 * index) }}
                  >
                    <motion.div 
                      className={`h-full ${stat.trend === 'up' ? 'bg-green-500' : 'bg-red-500'}`}
                      initial={{ width: 0 }}
                      animate={visible[1] ? { width: '70%' } : {}}
                      transition={{ duration: 1.2, delay: 0.7 + (0.1 * index) }}
                    />
                  </motion.div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Animated Population Trend Chart */}
      <section className="py-16 bg-white animate-on-scroll">
        <div className="container mx-auto px-4">
          <div className={cn(
            "transform transition-all duration-700 delay-200",
            visible[1] ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
          )}>
            <h2 className="mb-8 text-center text-3xl font-bold">
              <span className="relative inline-block">
                <span className="relative z-10">Population Growth Trends</span>
                <span className="absolute bottom-0 left-0 h-3 w-full bg-blue-100 z-0"></span>
              </span>
            </h2>
            
            <div className="grid gap-6 md:grid-cols-2">
              <motion.div 
                className="bg-white p-6 rounded-xl shadow-lg"
                initial={{ opacity: 0, x: -20 }}
                animate={visible[1] ? { opacity: 1, x: 0 } : {}}
                transition={{ duration: 0.5, delay: 0.3 }}
              >
                <h3 className="text-lg font-medium mb-4 text-gray-700">Population Growth (Millions)</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart
                      data={populationTrendData}
                      margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                    >
                      <defs>
                        <linearGradient id="colorPopulation" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#3B82F6" stopOpacity={0.1}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                      <XAxis dataKey="year" />
                      <YAxis domain={[14, 17]} />
                      <Tooltip 
                        formatter={(value) => [`${value}M`, 'Population']}
                        contentStyle={{ 
                          backgroundColor: 'rgba(255, 255, 255, 0.9)',
                          borderRadius: '8px',
                          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                          border: 'none'
                        }}
                      />
                      <Area 
                        type="monotone" 
                        dataKey="population" 
                        stroke="#3B82F6" 
                        fillOpacity={1} 
                        fill="url(#colorPopulation)" 
                        strokeWidth={2}
                        activeDot={{ r: 6, fill: '#3B82F6', stroke: '#fff', strokeWidth: 2 }}
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
                <p className="text-sm text-gray-500 mt-4">Source: Somalia National Bureau of Statistics, Annual Population Report</p>
              </motion.div>
              
              <motion.div 
                className="flex flex-col justify-center px-6"
                initial={{ opacity: 0, x: 20 }}
                animate={visible[1] ? { opacity: 1, x: 0 } : {}}
                transition={{ duration: 0.5, delay: 0.5 }}
              >
                <h3 className="text-xl font-semibold mb-4">Understanding Our Growth</h3>
                <p className="text-gray-600 mb-6">
                  Somalia's population has been steadily increasing at an average rate of 2.9% annually over the last five years.
                  This growth presents both opportunities and challenges for our economic and social development.
                </p>
                <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                  <h4 className="font-medium text-blue-700 mb-2">Key Insights:</h4>
                  <ul className="list-disc pl-5 space-y-2 text-gray-700">
                    <li>Urban population growing faster than rural areas</li>
                    <li>Youth (under 25) make up approximately 60% of the population</li>
                    <li>Mogadishu remains the most densely populated area</li>
                    <li>Internal migration continues to impact regional demographics</li>
                  </ul>
                </div>
              </motion.div>
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

      {/* Economic Data Visualizations */}
      <section className="py-20 bg-gradient-to-b from-blue-50 to-white animate-on-scroll">
        <div className="container mx-auto px-4">
          <div className={cn(
            "transform transition-all duration-700 delay-300",
            visible[2] ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
          )}>
            <h2 className="mb-10 text-center text-3xl font-bold">
              <span className="relative inline-block">
                <span className="relative z-10">Economic Development</span>
                <span className="absolute bottom-0 left-0 h-3 w-full bg-blue-100 z-0"></span>
              </span>
            </h2>
            
            <div className="grid gap-8 md:grid-cols-2 xl:grid-cols-3">
              {/* GDP Growth Chart */}
              <motion.div 
                className="md:col-span-2 xl:col-span-2 bg-white p-6 rounded-xl shadow-lg"
                initial={{ opacity: 0, y: 20 }}
                animate={visible[2] ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.6 }}
              >
                <h3 className="text-lg font-medium mb-4 text-gray-700">GDP Growth (Billion USD)</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={gdpData}
                      margin={{ top: 10, right: 30, left: 10, bottom: 10 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
                      <XAxis dataKey="year" />
                      <YAxis domain={[7, 8.5]} />
                      <Tooltip 
                        formatter={(value) => [`$${value}B`, 'GDP']}
                        contentStyle={{ 
                          backgroundColor: 'rgba(255, 255, 255, 0.9)',
                          borderRadius: '8px',
                          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                          border: 'none'
                        }}
                      />
                      <Bar 
                        dataKey="gdp" 
                        fill="#3B82F6" 
                        radius={[4, 4, 0, 0]}
                        animationDuration={1500}
                        barSize={40}
                      >
                        {gdpData.map((entry, index) => (
                          <Cell 
                            key={`cell-${index}`} 
                            fill={`rgba(59, 130, 246, ${0.7 + (index * 0.05)})`} 
                          />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
                <div className="flex justify-between mt-4 text-sm text-gray-500">
                  <p>Source: Central Bank of Somalia, Annual Report</p>
                  <p className="font-medium text-blue-600">GDP growth trend: +4.2% YoY</p>
                </div>
              </motion.div>
              
              {/* Economic Sectors Pie Chart */}
              <motion.div 
                className="bg-white p-6 rounded-xl shadow-lg"
                initial={{ opacity: 0, y: 20 }}
                animate={visible[2] ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                <h3 className="text-lg font-medium mb-4 text-gray-700">Economic Sector Contribution (%)</h3>
                <div className="h-64 flex justify-center items-center">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Tooltip 
                        formatter={(value) => [`${value}%`, 'Contribution']}
                        contentStyle={{ 
                          backgroundColor: 'rgba(255, 255, 255, 0.9)',
                          borderRadius: '8px',
                          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                          border: 'none'
                        }}
                      />
                      <Pie
                        data={sectorContributionData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={80}
                        paddingAngle={5}
                        dataKey="value"
                        animationDuration={1500}
                        animationBegin={300}
                      >
                        {sectorContributionData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                    </PieChart>
                  </ResponsiveContainer>
                </div>
                <div className="mt-4 grid grid-cols-3 gap-2">
                  {sectorContributionData.map((entry, index) => (
                    <div key={index} className="flex items-center">
                      <div
                        className="h-3 w-3 rounded-full mr-2"
                        style={{ backgroundColor: COLORS[index % COLORS.length] }}
                      />
                      <span className="text-sm text-gray-600">{entry.name} ({entry.value}%)</span>
                    </div>
                  ))}
                </div>
                <p className="text-sm text-gray-500 mt-4">Source: National Economic Survey</p>
              </motion.div>
            </div>
            
            <motion.div 
              className="mt-10 bg-blue-50 p-6 rounded-xl border border-blue-100 shadow-sm"
              initial={{ opacity: 0, y: 20 }}
              animate={visible[2] ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              <h3 className="font-medium text-blue-800 mb-2">Economic Outlook Summary</h3>
              <p className="text-gray-700">
                Somalia's economy continues to show resilience and growth despite global challenges. The agricultural sector remains
                the backbone of the economy, with services growing rapidly, particularly in urban areas. Foreign investments have 
                increased by 15% in the last year, primarily in infrastructure and telecommunications sectors.
              </p>
            </motion.div>
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
                  <span className="relative z-10">Interactive Map & Live Data</span>
                  <span className="absolute bottom-0 left-0 h-3 w-full bg-blue-100 z-0"></span>
                </span>
              </h2>
              <p className="mb-6 max-w-2xl text-center text-gray-600 leading-relaxed">
                Explore Somalia's regional statistics with our interactive map and watch live data updates from our monitoring systems.
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
              {/* Map Column */}
              <motion.div 
                className="lg:col-span-3 rounded-xl overflow-hidden shadow-xl border border-gray-200"
                initial={{ opacity: 0, x: -20 }}
                animate={visible[3] ? { opacity: 1, x: 0 } : {}}
                transition={{ duration: 0.5 }}
              >
                <SomaliaMap 
                  selectedRegion="all" 
                  onRegionSelect={(regionCode) => {
                    console.log('Selected region:', regionCode);
                    // This is just for demonstration in the landing page
                    // We don't actually change the region selection here
                  }}
                  height="500px"
                />
              </motion.div>

              {/* Live Data Column */}
              <motion.div 
                className="lg:col-span-2 bg-white rounded-xl shadow-xl border border-gray-200 p-6 flex flex-col"
                initial={{ opacity: 0, x: 20 }}
                animate={visible[3] ? { opacity: 1, x: 0 } : {}}
                transition={{ duration: 0.5, delay: 0.2 }}
              >
                <h3 className="text-lg font-medium mb-4 text-gray-700 flex items-center">
                  <span className="mr-2">Live Data Feed</span>
                  <motion.div 
                    className="h-2 w-2 rounded-full bg-green-500" 
                    animate={{ 
                      scale: [1, 1.5, 1],
                      opacity: [1, 0.8, 1] 
                    }}
                    transition={{ duration: 2, repeat: Infinity }}
                  />
                </h3>

                <div className="h-64 mb-4">
                  <ResponsiveContainer width="100%" height="100%">
                    <RechartsLineChart
                      data={liveData}
                      margin={{ top: 10, right: 10, left: 0, bottom: 0 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
                      <XAxis dataKey="time" />
                      <YAxis domain={[50, 100]} />
                      <Tooltip
                        contentStyle={{ 
                          backgroundColor: 'rgba(255, 255, 255, 0.9)',
                          borderRadius: '8px',
                          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
                          border: 'none'
                        }}
                      />
                      <defs>
                        <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#10B981" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#10B981" stopOpacity={0.1}/>
                        </linearGradient>
                      </defs>
                      <Line 
                        type="monotone" 
                        dataKey="value" 
                        stroke="#10B981" 
                        strokeWidth={2}
                        dot={{ r: 4, fill: '#10B981', stroke: '#fff', strokeWidth: 2 }}
                        activeDot={{ r: 6, fill: '#10B981', stroke: '#fff', strokeWidth: 2 }}
                        isAnimationActive={true}
                      />
                    </RechartsLineChart>
                  </ResponsiveContainer>
                </div>

                <div className="space-y-3 flex-grow">
                  {/* Animated data feed entries */}
                  {[
                    { time: '14 min ago', event: 'Temperature data updated for Mogadishu', value: '28°C' },
                    { time: '36 min ago', event: 'Rainfall data updated for Baidoa', value: '3.2mm' },
                    { time: '1 hour ago', event: 'Agricultural yield report from Kismayo', value: '+4.5%' },
                  ].map((item, index) => (
                    <motion.div 
                      key={index}
                      className="p-3 bg-gray-50 rounded-lg border border-gray-100 flex justify-between items-center"
                      initial={{ opacity: 0, y: 10 }}
                      animate={visible[3] ? { opacity: 1, y: 0 } : {}}
                      transition={{ duration: 0.3, delay: 0.4 + (index * 0.1) }}
                    >
                      <div>
                        <div className="flex items-center">
                          <span className="h-2 w-2 bg-blue-500 rounded-full mr-2"></span>
                          <span className="text-xs text-gray-500">{item.time}</span>
                        </div>
                        <p className="text-sm font-medium text-gray-700">{item.event}</p>
                      </div>
                      <span className="font-bold text-green-600">{item.value}</span>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
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
            visible[4] ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
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
                    <div className="mt-2 sm:mt-0 text-sm text-gray-500 flex items-center">
                      <LucideLineChart className="h-3 w-3 mr-1" />
                      {update.date}
                    </div>
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
