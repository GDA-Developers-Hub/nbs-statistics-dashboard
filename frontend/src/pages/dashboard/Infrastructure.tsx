import React, { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import GlobalFilters from '@/components/filters/GlobalFilters'
import SomaliaMap from '@/components/map/SomaliaMap'

// Mock data for infrastructure indicators
const infrastructureIndicators = [
  {
    id: 1,
    category: 'Energy',
    indicator: 'Access to Electricity',
    value: '32.6%',
    year: 2025,
    change: '+2.8%',
    trend: 'increasing'
  },
  {
    id: 2,
    category: 'Energy',
    indicator: 'Urban Electricity Access',
    value: '65.8%',
    year: 2025,
    change: '+3.2%',
    trend: 'increasing'
  },
  {
    id: 3,
    category: 'Energy',
    indicator: 'Rural Electricity Access',
    value: '12.5%',
    year: 2025,
    change: '+1.6%',
    trend: 'increasing'
  },
  {
    id: 4,
    category: 'Water',
    indicator: 'Access to Safe Water',
    value: '56.4%',
    year: 2025,
    change: '+3.2%',
    trend: 'increasing'
  },
  {
    id: 5,
    category: 'Water',
    indicator: 'Urban Water Access',
    value: '73.1%',
    year: 2025,
    change: '+2.5%',
    trend: 'increasing'
  },
  {
    id: 6,
    category: 'Water',
    indicator: 'Rural Water Access',
    value: '34.8%',
    year: 2025,
    change: '+3.6%',
    trend: 'increasing'
  },
  {
    id: 7,
    category: 'Transportation',
    indicator: 'Paved Roads',
    value: '2,860 km',
    year: 2025,
    change: '+120 km',
    trend: 'increasing'
  },
  {
    id: 8,
    category: 'Transportation',
    indicator: 'Functioning Ports',
    value: '4',
    year: 2025,
    change: '0',
    trend: 'stable'
  },
  {
    id: 9,
    category: 'Transportation',
    indicator: 'Functioning Airports',
    value: '6',
    year: 2025,
    change: '+1',
    trend: 'increasing'
  },
  {
    id: 10,
    category: 'Telecommunications',
    indicator: 'Mobile Penetration',
    value: '78.3%',
    year: 2025,
    change: '+5.1%',
    trend: 'increasing'
  },
  {
    id: 11,
    category: 'Telecommunications',
    indicator: 'Internet Penetration',
    value: '24.6%',
    year: 2025,
    change: '+3.8%',
    trend: 'increasing'
  },
  {
    id: 12,
    category: 'Telecommunications',
    indicator: 'Broadband Subscriptions',
    value: '1.2%',
    year: 2025,
    change: '+0.4%',
    trend: 'increasing'
  }
]

// Mock data for access to basic infrastructure by region
const regionalAccess = [
  { region: 'Banaadir', electricity: 82.5, water: 85.2, roads: 70.5, telecom: 95.3 },
  { region: 'Jubaland', electricity: 23.8, water: 42.1, roads: 18.6, telecom: 68.7 },
  { region: 'Puntland', electricity: 37.2, water: 63.4, roads: 34.2, telecom: 77.8 },
  { region: 'Galmudug', electricity: 21.5, water: 48.3, roads: 15.8, telecom: 65.1 },
  { region: 'Hirshabelle', electricity: 18.9, water: 45.7, roads: 12.3, telecom: 62.8 },
  { region: 'South West', electricity: 25.3, water: 51.2, roads: 21.7, telecom: 71.4 }
]

const Infrastructure = () => {
  const [region, setRegion] = useState('all')
  const [sector, setSector] = useState('all')
  const [timePeriod, setTimePeriod] = useState('all')
  
  const handleRegionSelect = (regionCode: string) => {
    setRegion(regionCode)
  }
  
  // Filter data based on selected region
  const filteredRegionalData = region === 'all' 
    ? regionalAccess 
    : regionalAccess.filter(item => item.region.toLowerCase().replace(' ', '').includes(region))

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Infrastructure</h1>
      
      {/* Global filters */}
      <GlobalFilters 
        region={region}
        setRegion={setRegion}
        sector={sector}
        setSector={setSector}
        timePeriod={timePeriod}
        setTimePeriod={setTimePeriod}
      />
      
      <div className="grid gap-6 md:grid-cols-2">
        {/* Somalia Map for geographical filtering */}
        <div>
          <SomaliaMap 
            selectedRegion={region} 
            onRegionSelect={handleRegionSelect} 
          />
        </div>
        
        {/* Infrastructure Overview Card */}
        <Card>
          <CardHeader>
            <CardTitle>Infrastructure Access Overview</CardTitle>
            <CardDescription>Key nationwide access indicators (2025)</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4">
              <div className="rounded-lg bg-blue-50 p-4 text-center">
                <div className="text-sm font-medium text-blue-600">Electricity Access</div>
                <div className="mt-1 text-2xl font-bold">32.6%</div>
                <div className="text-xs text-green-600">+2.8% from last year</div>
              </div>
              <div className="rounded-lg bg-green-50 p-4 text-center">
                <div className="text-sm font-medium text-green-600">Safe Water Access</div>
                <div className="mt-1 text-2xl font-bold">56.4%</div>
                <div className="text-xs text-green-600">+3.2% from last year</div>
              </div>
              <div className="rounded-lg bg-amber-50 p-4 text-center">
                <div className="text-sm font-medium text-amber-600">Paved Roads</div>
                <div className="mt-1 text-2xl font-bold">2,860 km</div>
                <div className="text-xs text-green-600">+120 km from last year</div>
              </div>
              <div className="rounded-lg bg-purple-50 p-4 text-center">
                <div className="text-sm font-medium text-purple-600">Mobile Penetration</div>
                <div className="mt-1 text-2xl font-bold">78.3%</div>
                <div className="text-xs text-green-600">+5.1% from last year</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
      
      {/* Regional Access Table */}
      <Card>
        <CardHeader>
          <CardTitle>Regional Infrastructure Access</CardTitle>
          <CardDescription>
            Access to basic infrastructure by region (%, 2025)
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-100 text-left">
                  <th className="p-2 border-b border-gray-200 text-gray-600 font-medium">Region</th>
                  <th className="p-2 border-b border-gray-200 text-gray-600 font-medium">Electricity Access</th>
                  <th className="p-2 border-b border-gray-200 text-gray-600 font-medium">Safe Water Access</th>
                  <th className="p-2 border-b border-gray-200 text-gray-600 font-medium">Road Network</th>
                  <th className="p-2 border-b border-gray-200 text-gray-600 font-medium">Telecom Coverage</th>
                </tr>
              </thead>
              <tbody>
                {filteredRegionalData.map((item) => (
                  <tr key={item.region} className="hover:bg-gray-50">
                    <td className="p-2 border-b border-gray-200 font-medium">{item.region}</td>
                    <td className="p-2 border-b border-gray-200">
                      <div className="flex items-center">
                        <span className="mr-2">{item.electricity}%</span>
                        <div className="w-24 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-blue-600 h-2 rounded-full" 
                            style={{ width: `${item.electricity}%` }}
                          ></div>
                        </div>
                      </div>
                    </td>
                    <td className="p-2 border-b border-gray-200">
                      <div className="flex items-center">
                        <span className="mr-2">{item.water}%</span>
                        <div className="w-24 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-green-600 h-2 rounded-full" 
                            style={{ width: `${item.water}%` }}
                          ></div>
                        </div>
                      </div>
                    </td>
                    <td className="p-2 border-b border-gray-200">
                      <div className="flex items-center">
                        <span className="mr-2">{item.roads}%</span>
                        <div className="w-24 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-amber-600 h-2 rounded-full" 
                            style={{ width: `${item.roads}%` }}
                          ></div>
                        </div>
                      </div>
                    </td>
                    <td className="p-2 border-b border-gray-200">
                      <div className="flex items-center">
                        <span className="mr-2">{item.telecom}%</span>
                        <div className="w-24 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-purple-600 h-2 rounded-full" 
                            style={{ width: `${item.telecom}%` }}
                          ></div>
                        </div>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
      
      {/* Infrastructure indicators table */}
      <Card>
        <CardHeader>
          <CardTitle>Infrastructure Indicators</CardTitle>
          <CardDescription>
            Detailed infrastructure statistics {region !== 'all' ? `for selected region` : 'nationwide'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-100 text-left">
                  <th className="p-2 border-b border-gray-200 text-gray-600 font-medium">Category</th>
                  <th className="p-2 border-b border-gray-200 text-gray-600 font-medium">Indicator</th>
                  <th className="p-2 border-b border-gray-200 text-gray-600 font-medium">Value</th>
                  <th className="p-2 border-b border-gray-200 text-gray-600 font-medium">Year</th>
                  <th className="p-2 border-b border-gray-200 text-gray-600 font-medium">Change</th>
                </tr>
              </thead>
              <tbody>
                {infrastructureIndicators.map((indicator) => (
                  <tr key={indicator.id} className="hover:bg-gray-50">
                    <td className="p-2 border-b border-gray-200">{indicator.category}</td>
                    <td className="p-2 border-b border-gray-200 font-medium">{indicator.indicator}</td>
                    <td className="p-2 border-b border-gray-200">{indicator.value}</td>
                    <td className="p-2 border-b border-gray-200">{indicator.year}</td>
                    <td className="p-2 border-b border-gray-200">
                      <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                        indicator.trend === 'increasing' ? 'bg-green-100 text-green-800' : 
                        indicator.trend === 'stable' ? 'bg-gray-100 text-gray-800' : 
                        'bg-red-100 text-red-800'
                      }`}>
                        {indicator.change}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Infrastructure
