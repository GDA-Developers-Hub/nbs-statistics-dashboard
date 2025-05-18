import React, { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import GlobalFilters from '@/components/filters/GlobalFilters'
import SomaliaMap from '@/components/map/SomaliaMap'
import LiteracyRateChart from '@/components/charts/LiteracyRateChart'
import VaccinationCoverageChart from '@/components/charts/VaccinationCoverageChart'

// Mock data for social development indicators
const socialIndicators = [
  {
    id: 1,
    category: 'Education',
    indicator: 'Literacy Rate',
    value: '45.0%',
    year: 2025,
    change: '+3.0%',
    trend: 'increasing'
  },
  {
    id: 2,
    category: 'Education',
    indicator: 'Primary School Enrollment',
    value: '76.5%',
    year: 2025,
    change: '+3.1%',
    trend: 'increasing'
  },
  {
    id: 3,
    category: 'Education',
    indicator: 'Secondary School Enrollment',
    value: '32.4%',
    year: 2025,
    change: '+2.8%',
    trend: 'increasing'
  },
  {
    id: 4,
    category: 'Education',
    indicator: 'Student-Teacher Ratio (Primary)',
    value: '36:1',
    year: 2025,
    change: '-2.0',
    trend: 'decreasing'
  },
  {
    id: 5,
    category: 'Health',
    indicator: 'Life Expectancy',
    value: '57.2 years',
    year: 2025,
    change: '+0.8',
    trend: 'increasing'
  },
  {
    id: 6,
    category: 'Health',
    indicator: 'Infant Mortality',
    value: '72/1,000',
    year: 2025,
    change: '-3.4',
    trend: 'decreasing'
  },
  {
    id: 7,
    category: 'Health',
    indicator: 'Maternal Mortality',
    value: '732/100,000',
    year: 2025,
    change: '-18.0',
    trend: 'decreasing'
  },
  {
    id: 8,
    category: 'Health',
    indicator: 'Vaccination Coverage',
    value: '67.0%',
    year: 2025,
    change: '+2.0%',
    trend: 'increasing'
  },
  {
    id: 9,
    category: 'Health',
    indicator: 'Malnutrition (Children under 5)',
    value: '12.7%',
    year: 2025,
    change: '-1.5%',
    trend: 'decreasing'
  },
  {
    id: 10,
    category: 'Health',
    indicator: 'Access to Safe Water',
    value: '56.4%',
    year: 2025,
    change: '+3.2%',
    trend: 'increasing'
  }
]

const SocialDevelopment = () => {
  const [region, setRegion] = useState('all')
  const [sector, setSector] = useState('all')
  const [timePeriod, setTimePeriod] = useState('all')

  const handleRegionSelect = (regionCode: string) => {
    setRegion(regionCode)
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Social Development</h1>
      
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
        
        {/* Summary statistics card */}
        <Card>
          <CardHeader>
            <CardTitle>Social Development Overview</CardTitle>
            <CardDescription>Key social indicators summary</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4">
              <div className="rounded-lg bg-blue-50 p-4 text-center">
                <div className="text-sm font-medium text-blue-600">Literacy Rate</div>
                <div className="mt-1 text-2xl font-bold">45.0%</div>
                <div className="text-xs text-green-600">+3.0% from last year</div>
              </div>
              <div className="rounded-lg bg-green-50 p-4 text-center">
                <div className="text-sm font-medium text-green-600">Life Expectancy</div>
                <div className="mt-1 text-2xl font-bold">57.2 years</div>
                <div className="text-xs text-green-600">+0.8 from last year</div>
              </div>
              <div className="rounded-lg bg-purple-50 p-4 text-center">
                <div className="text-sm font-medium text-purple-600">School Enrollment</div>
                <div className="mt-1 text-2xl font-bold">76.5%</div>
                <div className="text-xs text-green-600">+3.1% from last year</div>
              </div>
              <div className="rounded-lg bg-amber-50 p-4 text-center">
                <div className="text-sm font-medium text-amber-600">Vaccination Coverage</div>
                <div className="mt-1 text-2xl font-bold">67.0%</div>
                <div className="text-xs text-green-600">+2.0% from last year</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
      
      <div className="grid gap-6 md:grid-cols-2">
        {/* Literacy Rate Chart */}
        <div>
          <LiteracyRateChart />
        </div>
        
        {/* Vaccination Coverage Chart */}
        <div>
          <VaccinationCoverageChart />
        </div>
      </div>
      
      {/* Social indicators table */}
      <Card>
        <CardHeader>
          <CardTitle>Social Development Indicators</CardTitle>
          <CardDescription>
            Key education and health statistics {region !== 'all' ? `for selected region` : 'nationwide'}
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
                {socialIndicators.map((indicator) => (
                  <tr key={indicator.id} className="hover:bg-gray-50">
                    <td className="p-2 border-b border-gray-200">{indicator.category}</td>
                    <td className="p-2 border-b border-gray-200 font-medium">{indicator.indicator}</td>
                    <td className="p-2 border-b border-gray-200">{indicator.value}</td>
                    <td className="p-2 border-b border-gray-200">{indicator.year}</td>
                    <td className="p-2 border-b border-gray-200">
                      <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                        indicator.trend === 'increasing' 
                          ? indicator.category === 'Health' && indicator.indicator.includes('Mortality')
                            ? 'bg-red-100 text-red-800'
                            : 'bg-green-100 text-green-800'
                          : indicator.category === 'Health' && indicator.indicator.includes('Mortality')
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
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

export default SocialDevelopment
