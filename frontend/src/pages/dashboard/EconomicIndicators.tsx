import React, { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import GlobalFilters from '@/components/filters/GlobalFilters'
import SomaliaMap from '@/components/map/SomaliaMap'
import CPITrendsChart from '@/components/charts/CPITrendsChart'

// Mock data for economic indicators
const economicIndicators = [
  {
    id: 1,
    category: 'Economic Growth',
    indicator: 'GDP',
    value: '$7.3 billion',
    year: 2024,
    change: '+3.2%',
    trend: 'increasing'
  },
  {
    id: 2,
    category: 'Economic Growth',
    indicator: 'GDP Per Capita',
    value: '$431',
    year: 2024,
    change: '+2.1%',
    trend: 'increasing'
  },
  {
    id: 3,
    category: 'Economic Growth',
    indicator: 'GDP Growth Rate',
    value: '3.2%',
    year: 2024,
    change: '+0.3%',
    trend: 'increasing'
  },
  {
    id: 4,
    category: 'Inflation',
    indicator: 'Inflation Rate',
    value: '4.1%',
    year: 2024,
    change: '-0.3%',
    trend: 'decreasing'
  },
  {
    id: 5,
    category: 'Inflation',
    indicator: 'Food Inflation',
    value: '5.2%',
    year: 2024,
    change: '-0.5%',
    trend: 'decreasing'
  },
  {
    id: 6,
    category: 'Trade',
    indicator: 'Exports',
    value: '$658 million',
    year: 2024,
    change: '+4.5%',
    trend: 'increasing'
  },
  {
    id: 7,
    category: 'Trade',
    indicator: 'Imports',
    value: '$3.1 billion',
    year: 2024,
    change: '+2.8%',
    trend: 'increasing'
  },
  {
    id: 8,
    category: 'Trade',
    indicator: 'Trade Balance',
    value: '-$2.4 billion',
    year: 2024,
    change: '+1.2%',
    trend: 'increasing'
  },
  {
    id: 9,
    category: 'Finance',
    indicator: 'Foreign Direct Investment',
    value: '$412 million',
    year: 2024,
    change: '+2.3%',
    trend: 'increasing'
  },
  {
    id: 10,
    category: 'Finance',
    indicator: 'Remittances',
    value: '$1.7 billion',
    year: 2024,
    change: '+1.8%',
    trend: 'increasing'
  }
]

// Mock data for sectoral GDP contribution
const sectoralGDP = [
  { sector: 'Agriculture', percentage: 58.9 },
  { sector: 'Industry', percentage: 9.5 },
  { sector: 'Services', percentage: 31.6 }
]

const EconomicIndicators = () => {
  const [region, setRegion] = useState('all')
  const [sector, setSector] = useState('all')
  const [timePeriod, setTimePeriod] = useState('all')

  const handleRegionSelect = (regionCode: string) => {
    setRegion(regionCode)
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Economic Indicators</h1>
      
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
        
        {/* CPI Trends Chart */}
        <div>
          <CPITrendsChart />
        </div>
      </div>
      
      {/* Sectoral GDP Contribution */}
      <Card>
        <CardHeader>
          <CardTitle>Sectoral GDP Contribution</CardTitle>
          <CardDescription>Percentage contribution to GDP by major economic sectors (2024)</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-100 text-left">
                  <th className="p-2 border-b border-gray-200 text-gray-600 font-medium">Sector</th>
                  <th className="p-2 border-b border-gray-200 text-gray-600 font-medium">GDP Contribution</th>
                  <th className="p-2 border-b border-gray-200 text-gray-600 font-medium">Visualization</th>
                </tr>
              </thead>
              <tbody>
                {sectoralGDP.map((item) => (
                  <tr key={item.sector} className="hover:bg-gray-50">
                    <td className="p-2 border-b border-gray-200 font-medium">{item.sector}</td>
                    <td className="p-2 border-b border-gray-200">{item.percentage}%</td>
                    <td className="p-2 border-b border-gray-200">
                      <div className="w-full bg-gray-200 rounded-full h-2.5">
                        <div 
                          className="bg-blue-600 h-2.5 rounded-full" 
                          style={{ width: `${item.percentage}%` }}
                        ></div>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
      
      {/* Economic key indicators */}
      <Card>
        <CardHeader>
          <CardTitle>Economic Indicators</CardTitle>
          <CardDescription>
            Key economic statistics {region !== 'all' ? `for selected region` : 'nationwide'}
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
                {economicIndicators.map((indicator) => (
                  <tr key={indicator.id} className="hover:bg-gray-50">
                    <td className="p-2 border-b border-gray-200">{indicator.category}</td>
                    <td className="p-2 border-b border-gray-200 font-medium">{indicator.indicator}</td>
                    <td className="p-2 border-b border-gray-200">{indicator.value}</td>
                    <td className="p-2 border-b border-gray-200">{indicator.year}</td>
                    <td className="p-2 border-b border-gray-200">
                      <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                        indicator.trend === 'increasing' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
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

export default EconomicIndicators
