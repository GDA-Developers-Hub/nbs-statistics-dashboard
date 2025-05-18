import React from 'react'
import { AreaChart, Area, BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { ArrowDown, ArrowUp, Minus } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import MapDashboard from '@/components/dashboard/MapDashboard'

// Mock data for charts according to project requirements
const populationData = [
  { year: 2018, population: 14.7, growthRate: 2.9 },
  { year: 2019, population: 15.0, growthRate: 3.0 },
  { year: 2020, population: 15.4, growthRate: 2.8 },
  { year: 2021, population: 15.8, growthRate: 2.7 },
  { year: 2022, population: 16.1, growthRate: 2.6 },
  { year: 2023, population: 16.5, growthRate: 2.5 },
  { year: 2024, population: 16.9, growthRate: 2.4 },
  { year: 2025, population: 17.3, growthRate: 2.3 },
]

const literacyData = [
  { year: 2018, rate: 30 },
  { year: 2019, rate: 32 },
  { year: 2020, rate: 34 },
  { year: 2021, rate: 36 },
  { year: 2022, rate: 37 },
  { year: 2023, rate: 39 },
  { year: 2024, rate: 42 },
  { year: 2025, rate: 45 },
]

const vaccinationData = [
  { year: 2018, coverage: 45 },
  { year: 2019, coverage: 52 },
  { year: 2020, coverage: 48 },
  { year: 2021, coverage: 56 },
  { year: 2022, coverage: 60 },
  { year: 2023, coverage: 65 },
  { year: 2024, coverage: 67 },
  { year: 2025, coverage: 70 },
]

const cpiData = [
  { year: 2018, quarter: 'Q1', cpi: 100 },
  { year: 2018, quarter: 'Q2', cpi: 102 },
  { year: 2018, quarter: 'Q3', cpi: 103 },
  { year: 2018, quarter: 'Q4', cpi: 105 },
  { year: 2019, quarter: 'Q1', cpi: 106 },
  { year: 2019, quarter: 'Q2', cpi: 108 },
  { year: 2019, quarter: 'Q3', cpi: 110 },
  { year: 2019, quarter: 'Q4', cpi: 112 },
  { year: 2020, quarter: 'Q1', cpi: 114 },
  { year: 2020, quarter: 'Q2', cpi: 118 },
  { year: 2020, quarter: 'Q3', cpi: 120 },
  { year: 2020, quarter: 'Q4', cpi: 122 },
  { year: 2021, quarter: 'Q1', cpi: 124 },
  { year: 2021, quarter: 'Q2', cpi: 126 },
  { year: 2021, quarter: 'Q3', cpi: 128 },
  { year: 2021, quarter: 'Q4', cpi: 130 },
  { year: 2022, quarter: 'Q1', cpi: 134 },
  { year: 2022, quarter: 'Q2', cpi: 138 },
  { year: 2022, quarter: 'Q3', cpi: 140 },
  { year: 2022, quarter: 'Q4', cpi: 142 },
  { year: 2023, quarter: 'Q1', cpi: 144 },
  { year: 2023, quarter: 'Q2', cpi: 146 },
  { year: 2023, quarter: 'Q3', cpi: 148 },
  { year: 2023, quarter: 'Q4', cpi: 150 },
  { year: 2024, quarter: 'Q1', cpi: 152 },
  { year: 2024, quarter: 'Q2', cpi: 154 },
  { year: 2024, quarter: 'Q3', cpi: 156 },
  { year: 2024, quarter: 'Q4', cpi: 158 },
  { year: 2025, quarter: 'Q1', cpi: 160 },
]

// Mock data for key indicators table
const indicators = [
  { id: 1, name: 'GDP Growth', value: '5.20%', change: 0.8, lastUpdated: 'Feb 2025' },
  { id: 2, name: 'Inflation', value: '7.10%', change: -0.5, lastUpdated: 'Feb 2025' },
  { id: 3, name: 'Foreign Investment', value: '$412M', change: 2.3, lastUpdated: 'Jan 2025' },
  { id: 4, name: 'Urban Population', value: '45.8%', change: 1.2, lastUpdated: 'Mar 2025' },
  { id: 5, name: 'Unemployment', value: '14.2%', change: -0.3, lastUpdated: 'Dec 2024' },
  { id: 6, name: 'Primary School Enrollment', value: '76.5%', change: 3.1, lastUpdated: 'Feb 2025' },
]

// Card component to wrap charts
const CardComponent = ({ title, description, children }: any) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent>{children}</CardContent>
    </Card>
  )
}

const Overview = () => {
  const [showGrowthRate, setShowGrowthRate] = React.useState(false)

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard Overview</h1>
      
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <CardComponent title="Total Population" description="Current population estimate">
          <div className="text-3xl font-bold">17.3M</div>
          <div className="text-sm text-green-600">+2.3% from last year</div>
        </CardComponent>
        
        <CardComponent title="GDP" description="Current GDP estimate">
          <div className="text-3xl font-bold">$8.4B</div>
          <div className="text-sm text-green-600">+5.2% annual growth</div>
        </CardComponent>
        
        <CardComponent title="Literacy Rate" description="Population aged 15+ who can read">
          <div className="text-3xl font-bold">45%</div>
          <div className="text-sm text-green-600">+3% from last year</div>
        </CardComponent>
        
        <CardComponent title="Life Expectancy" description="Average life expectancy">
          <div className="text-3xl font-bold">58.2</div>
          <div className="text-sm text-green-600">+0.8 years from 2023</div>
        </CardComponent>
      </div>
      
      {/* Key Statistical Indicators Table */}
      <Card>
        <CardHeader>
          <CardTitle>Key Statistical Indicators</CardTitle>
          <CardDescription>Latest available indicators</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="border-b">
                  <th className="py-3 text-left font-medium">Indicator</th>
                  <th className="py-3 text-left font-medium">Value</th>
                  <th className="py-3 text-left font-medium">Change %</th>
                  <th className="py-3 text-left font-medium">Last Updated</th>
                </tr>
              </thead>
              <tbody>
                {indicators.map((indicator) => (
                  <tr key={indicator.id} className="border-b hover:bg-gray-50">
                    <td className="py-3">{indicator.name}</td>
                    <td className="py-3 font-medium">{indicator.value}</td>
                    <td className="py-3">
                      <div className="flex items-center">
                        <span className={indicator.change > 0 ? 'text-green-600' : indicator.change < 0 ? 'text-red-600' : 'text-gray-500'}>
                          {indicator.change > 0 ? '+' : ''}{indicator.change}%
                        </span>
                        <span className="ml-2">
                          {indicator.change > 0 ? (
                            <ArrowUp className="h-4 w-4 text-green-600" />
                          ) : indicator.change < 0 ? (
                            <ArrowDown className="h-4 w-4 text-red-600" />
                          ) : (
                            <Minus className="h-4 w-4 text-gray-500" />
                          )}
                        </span>
                      </div>
                    </td>
                    <td className="py-3 text-gray-500">{indicator.lastUpdated}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
      
      {/* Charts Row */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Population Growth Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Population Growth</CardTitle>
            <CardDescription>
              <div className="flex items-center">
                <span>
                  {showGrowthRate ? 'Annual growth rate (%)' : 'Total population (millions)'}
                </span>
                <button
                  onClick={() => setShowGrowthRate(!showGrowthRate)}
                  className="ml-2 rounded-md bg-gray-100 px-2 py-1 text-xs font-medium hover:bg-gray-200"
                >
                  Switch to {showGrowthRate ? 'Population' : 'Growth Rate'}
                </button>
              </div>
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={populationData}
                  margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis 
                    domain={showGrowthRate ? [0, 10] : [0, 'auto']} 
                    tickFormatter={showGrowthRate ? (value) => `${value}%` : undefined}
                  />
                  <Tooltip formatter={(value) => showGrowthRate ? `${value}%` : value} />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey={showGrowthRate ? 'growthRate' : 'population'}
                    stroke="#3b82f6"
                    strokeWidth={2}
                    activeDot={{ r: 8 }}
                    name={showGrowthRate ? 'Growth Rate (%)' : 'Population (millions)'}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
        
        {/* Literacy Rate Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Literacy Rate</CardTitle>
            <CardDescription>Percentage of population aged 15+ who can read and write</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={literacyData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis domain={[0, 100]} tickFormatter={(value) => `${value}%`} />
                  <Tooltip formatter={(value) => `${value}%`} />
                  <Legend />
                  <Bar dataKey="rate" fill="#3b82f6" name="Literacy Rate (%)" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
        
        {/* Vaccination Coverage Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Vaccination Coverage</CardTitle>
            <CardDescription>Percentage of children fully vaccinated</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={vaccinationData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis domain={[0, 100]} tickFormatter={(value) => `${value}%`} />
                  <Tooltip formatter={(value) => `${value}%`} />
                  <Legend />
                  <Area type="monotone" dataKey="coverage" fill="rgba(59, 130, 246, 0.2)" stroke="#3b82f6" name="Coverage (%)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
        
        {/* CPI Trends Chart */}
        <Card>
          <CardHeader>
            <CardTitle>CPI Trends</CardTitle>
            <CardDescription>Consumer Price Index (base: 2018=100)</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={cpiData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="quarter" tickFormatter={(_, index) => {
                    const item = cpiData[index];
                    return `${item.year} ${item.quarter}`;
                  }} />
                  <YAxis />
                  <Tooltip labelFormatter={(_, data) => {
                    if (data && data.length > 0) {
                      const { year, quarter } = data[0].payload;
                      return `${year} ${quarter}`;
                    }
                    return '';
                  }} />
                  <Legend />
                  <Line type="monotone" dataKey="cpi" stroke="#3b82f6" name="CPI" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>
      
      {/* Regional Statistics Map Dashboard */}
      <div className="mt-8">
        <h2 className="text-xl font-bold mb-4">Regional Statistics</h2>
        <MapDashboard className="w-full" />
      </div>
    </div>
  )
}

export default Overview
