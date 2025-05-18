import React, { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import GlobalFilters from '@/components/filters/GlobalFilters'
import SomaliaMap from '@/components/map/SomaliaMap'
import PopulationGrowthChart from '@/components/charts/PopulationGrowthChart'
import KeyIndicatorsTable from '@/components/tables/KeyIndicatorsTable'

// Mock data for population statistics
const populationIndicators = [
  {
    id: 1,
    category: 'Demographics',
    indicator: 'Total Population',
    value: '17.3 million',
    year: 2025,
    change: '+2.3%',
    trend: 'increasing'
  },
  {
    id: 2,
    category: 'Demographics',
    indicator: 'Urban Population',
    value: '45.8%',
    year: 2025,
    change: '+1.2%',
    trend: 'increasing'
  },
  {
    id: 3,
    category: 'Demographics',
    indicator: 'Rural Population',
    value: '54.2%',
    year: 2025,
    change: '-1.2%',
    trend: 'decreasing'
  },
  {
    id: 4,
    category: 'Demographics',
    indicator: 'Population Density',
    value: '26.8 per km²',
    year: 2025,
    change: '+0.6',
    trend: 'increasing'
  },
  {
    id: 5,
    category: 'Demographics',
    indicator: 'Population Growth Rate',
    value: '2.3%',
    year: 2025,
    change: '-0.1%',
    trend: 'decreasing'
  },
  {
    id: 6,
    category: 'Age Structure',
    indicator: 'Population Under 15',
    value: '45.6%',
    year: 2025,
    change: '-0.3%',
    trend: 'decreasing'
  },
  {
    id: 7,
    category: 'Age Structure',
    indicator: 'Population 15-64',
    value: '51.5%',
    year: 2025,
    change: '+0.2%',
    trend: 'increasing'
  },
  {
    id: 8,
    category: 'Age Structure',
    indicator: 'Population 65+',
    value: '2.9%',
    year: 2025,
    change: '+0.1%',
    trend: 'increasing'
  },
]

const PopulationStatistics = () => {
  const [region, setRegion] = useState('all')
  const [sector, setSector] = useState('all')
  const [timePeriod, setTimePeriod] = useState('all')

  const handleRegionSelect = (regionCode: string) => {
    setRegion(regionCode)
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Population Statistics</h1>
      
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
        
        {/* Population Growth Chart */}
        <div>
          <PopulationGrowthChart />
        </div>
      </div>
      
      {/* Population key indicators */}
      <Card>
        <CardHeader>
          <CardTitle>Population Indicators</CardTitle>
          <CardDescription>
            Key population statistics {region !== 'all' ? `for selected region` : 'nationwide'}
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
                {populationIndicators.map((indicator) => (
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

export default PopulationStatistics
