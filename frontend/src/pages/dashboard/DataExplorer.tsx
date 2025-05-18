import React, { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import GlobalFilters from '@/components/filters/GlobalFilters'
import SomaliaMap from '@/components/map/SomaliaMap'
import { Bar, BarChart, Line, LineChart, CartesianGrid, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, ComposedChart, Area } from 'recharts'

// Mock data for various indicators
const mockedData = {
  // Population data over time
  populationTimeSeries: [
    { year: 2015, population: 14.1 },
    { year: 2016, population: 14.5 },
    { year: 2017, population: 14.9 },
    { year: 2018, population: 15.3 },
    { year: 2019, population: 15.7 },
    { year: 2020, population: 16.1 },
    { year: 2021, population: 16.5 },
    { year: 2022, population: 16.9 },
    { year: 2023, population: 17.3 },
    { year: 2024, population: 17.7 },
    { year: 2025, population: 18.1 }
  ],
  
  // Regional data
  regionalData: [
    { region: 'Banaadir', population: 2.8, gdp: 1.82, literacy: 65.3, healthcare: 62.8 },
    { region: 'Jubaland', population: 3.5, gdp: 0.85, literacy: 41.6, healthcare: 38.5 },
    { region: 'Puntland', population: 2.6, gdp: 0.92, literacy: 48.7, healthcare: 45.2 },
    { region: 'Galmudug', population: 2.4, gdp: 0.61, literacy: 38.4, healthcare: 35.6 },
    { region: 'Hirshabelle', population: 2.9, gdp: 0.68, literacy: 36.5, healthcare: 32.8 },
    { region: 'South West', population: 3.9, gdp: 0.88, literacy: 42.3, healthcare: 39.5 }
  ],
  
  // Economic indicators over time
  economicTimeSeries: [
    { year: 2015, gdp: 4.05, inflation: 4.0, exports: 0.42 },
    { year: 2016, gdp: 4.2, inflation: 4.5, exports: 0.45 },
    { year: 2017, gdp: 4.38, inflation: 5.2, exports: 0.47 },
    { year: 2018, gdp: 4.56, inflation: 4.8, exports: 0.51 },
    { year: 2019, gdp: 4.72, inflation: 4.5, exports: 0.54 },
    { year: 2020, gdp: 4.55, inflation: 5.6, exports: 0.48 },
    { year: 2021, gdp: 4.82, inflation: 6.1, exports: 0.52 },
    { year: 2022, gdp: 5.15, inflation: 7.3, exports: 0.58 },
    { year: 2023, gdp: 5.85, inflation: 6.5, exports: 0.61 },
    { year: 2024, gdp: 6.45, inflation: 5.8, exports: 0.64 },
    { year: 2025, gdp: 7.15, inflation: 5.2, exports: 0.68 }
  ],
  
  // Social indicators over time
  socialTimeSeries: [
    { year: 2015, literacy: 30, healthcare: 35, water: 42 },
    { year: 2016, literacy: 32, healthcare: 36, water: 44 },
    { year: 2017, literacy: 33, healthcare: 38, water: 46 },
    { year: 2018, literacy: 35, healthcare: 40, water: 48 },
    { year: 2019, literacy: 37, healthcare: 42, water: 50 },
    { year: 2020, literacy: 39, healthcare: 44, water: 52 },
    { year: 2021, literacy: 41, healthcare: 47, water: 54 },
    { year: 2022, literacy: 43, healthcare: 49, water: 56 },
    { year: 2023, literacy: 45, healthcare: 51, water: 58 },
    { year: 2024, literacy: 48, healthcare: 54, water: 61 },
    { year: 2025, literacy: 50, healthcare: 56, water: 63 }
  ]
}

// Available indicators for selection
const availableIndicators = [
  { id: 'population', name: 'Population', category: 'Demographics' },
  { id: 'gdp', name: 'GDP', category: 'Economy' },
  { id: 'inflation', name: 'Inflation Rate', category: 'Economy' },
  { id: 'exports', name: 'Exports', category: 'Economy' },
  { id: 'literacy', name: 'Literacy Rate', category: 'Social' },
  { id: 'healthcare', name: 'Healthcare Access', category: 'Social' },
  { id: 'water', name: 'Safe Water Access', category: 'Infrastructure' }
]

// Chart types
const chartTypes = [
  { id: 'line', name: 'Line Chart' },
  { id: 'bar', name: 'Bar Chart' },
  { id: 'area', name: 'Area Chart' },
  { id: 'composed', name: 'Composed Chart' }
]

// Supported views
const viewTypes = [
  { id: 'time', name: 'Time Series' },
  { id: 'regional', name: 'Regional Comparison' }
]

const DataExplorer = () => {
  const [region, setRegion] = useState('all')
  const [sector, setSector] = useState('all')
  const [timePeriod, setTimePeriod] = useState('all')
  
  // Data explorer specific state
  const [selectedView, setSelectedView] = useState('time')
  const [selectedChart, setSelectedChart] = useState('line')
  const [selectedIndicators, setSelectedIndicators] = useState(['population'])

  const handleRegionSelect = (regionCode: string) => {
    setRegion(regionCode)
  }

  // Toggle indicator selection
  const toggleIndicator = (indicatorId: string) => {
    if (selectedIndicators.includes(indicatorId)) {
      // Remove indicator if already selected
      setSelectedIndicators(selectedIndicators.filter(id => id !== indicatorId))
    } else {
      // Add indicator if not already selected (limit to 3 for readability)
      if (selectedIndicators.length < 3) {
        setSelectedIndicators([...selectedIndicators, indicatorId])
      }
    }
  }

  // Get appropriate data based on view type
  const getChartData = () => {
    if (selectedView === 'time') {
      // Combine data from different time series based on selected indicators
      return mockedData.populationTimeSeries.map(yearData => {
        const result: any = { year: yearData.year }
        
        if (selectedIndicators.includes('population')) {
          result.population = yearData.population
        }
        
        // Add economic indicators if selected
        if (selectedIndicators.some(id => ['gdp', 'inflation', 'exports'].includes(id))) {
          const economicData = mockedData.economicTimeSeries.find(d => d.year === yearData.year)
          if (economicData) {
            if (selectedIndicators.includes('gdp')) result.gdp = economicData.gdp
            if (selectedIndicators.includes('inflation')) result.inflation = economicData.inflation
            if (selectedIndicators.includes('exports')) result.exports = economicData.exports
          }
        }
        
        // Add social indicators if selected
        if (selectedIndicators.some(id => ['literacy', 'healthcare', 'water'].includes(id))) {
          const socialData = mockedData.socialTimeSeries.find(d => d.year === yearData.year)
          if (socialData) {
            if (selectedIndicators.includes('literacy')) result.literacy = socialData.literacy
            if (selectedIndicators.includes('healthcare')) result.healthcare = socialData.healthcare
            if (selectedIndicators.includes('water')) result.water = socialData.water
          }
        }
        
        return result
      })
    } else {
      // Filter regional data if a specific region is selected
      let data = mockedData.regionalData
      if (region !== 'all') {
        data = data.filter(r => r.region.toLowerCase().replace(' ', '').includes(region))
      }
      return data
    }
  }

  // Render appropriate chart based on selection
  const renderChart = () => {
    const data = getChartData()
    const height = 400
    
    // Get colors for selected indicators
    const getColor = (index: number) => {
      const colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899']
      return colors[index % colors.length]
    }
    
    // Set the appropriate keys and labels
    const xKey = selectedView === 'time' ? 'year' : 'region'
    
    // Create data key configs
    const dataKeys = selectedIndicators.map((indicator, index) => ({
      dataKey: indicator,
      name: availableIndicators.find(i => i.id === indicator)?.name || indicator,
      color: getColor(index)
    }))
    
    switch (selectedChart) {
      case 'line':
        return (
          <ResponsiveContainer width="100%" height={height}>
            <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={xKey} />
              <YAxis />
              <Tooltip />
              <Legend />
              {dataKeys.map((key, index) => (
                <Line 
                  key={key.dataKey}
                  type="monotone" 
                  dataKey={key.dataKey} 
                  name={key.name}
                  stroke={key.color}
                  activeDot={{ r: 8 }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        )
        
      case 'bar':
        return (
          <ResponsiveContainer width="100%" height={height}>
            <BarChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={xKey} />
              <YAxis />
              <Tooltip />
              <Legend />
              {dataKeys.map((key, index) => (
                <Bar 
                  key={key.dataKey}
                  dataKey={key.dataKey} 
                  name={key.name}
                  fill={key.color}
                />
              ))}
            </BarChart>
          </ResponsiveContainer>
        )
        
      case 'area':
        return (
          <ResponsiveContainer width="100%" height={height}>
            <ComposedChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={xKey} />
              <YAxis />
              <Tooltip />
              <Legend />
              {dataKeys.map((key, index) => (
                <Area 
                  key={key.dataKey}
                  type="monotone" 
                  dataKey={key.dataKey} 
                  name={key.name}
                  fill={key.color}
                  stroke={key.color}
                  fillOpacity={0.3}
                />
              ))}
            </ComposedChart>
          </ResponsiveContainer>
        )
        
      case 'composed':
        return (
          <ResponsiveContainer width="100%" height={height}>
            <ComposedChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={xKey} />
              <YAxis />
              <Tooltip />
              <Legend />
              {dataKeys.map((key, index) => {
                // Alternate between different chart types for composed chart
                switch (index % 3) {
                  case 0:
                    return (
                      <Line 
                        key={key.dataKey}
                        type="monotone" 
                        dataKey={key.dataKey} 
                        name={key.name}
                        stroke={key.color}
                      />
                    )
                  case 1:
                    return (
                      <Bar 
                        key={key.dataKey}
                        dataKey={key.dataKey} 
                        name={key.name}
                        fill={key.color}
                      />
                    )
                  case 2:
                    return (
                      <Area 
                        key={key.dataKey}
                        type="monotone" 
                        dataKey={key.dataKey} 
                        name={key.name}
                        fill={key.color}
                        stroke={key.color}
                        fillOpacity={0.3}
                      />
                    )
                  default:
                    return null
                }
              })}
            </ComposedChart>
          </ResponsiveContainer>
        )
        
      default:
        return <div>Please select a chart type</div>
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Data Explorer</h1>
      
      {/* Global filters */}
      <GlobalFilters 
        region={region}
        setRegion={setRegion}
        sector={sector}
        setSector={setSector}
        timePeriod={timePeriod}
        setTimePeriod={setTimePeriod}
      />
      
      <div className="grid gap-6 grid-cols-1 md:grid-cols-3">
        {/* Control panel */}
        <Card className="md:col-span-1">
          <CardHeader>
            <CardTitle>Chart Controls</CardTitle>
            <CardDescription>Customize your data visualization</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* View Type Selection */}
            <div>
              <h3 className="text-sm font-medium mb-2">View Type</h3>
              <div className="flex flex-wrap gap-2">
                {viewTypes.map(view => (
                  <button
                    key={view.id}
                    className={`px-3 py-1 rounded text-sm ${
                      selectedView === view.id 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-gray-100 hover:bg-gray-200'
                    }`}
                    onClick={() => setSelectedView(view.id)}
                  >
                    {view.name}
                  </button>
                ))}
              </div>
            </div>
            
            {/* Chart Type Selection */}
            <div>
              <h3 className="text-sm font-medium mb-2">Chart Type</h3>
              <div className="flex flex-wrap gap-2">
                {chartTypes.map(chart => (
                  <button
                    key={chart.id}
                    className={`px-3 py-1 rounded text-sm ${
                      selectedChart === chart.id 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-gray-100 hover:bg-gray-200'
                    }`}
                    onClick={() => setSelectedChart(chart.id)}
                  >
                    {chart.name}
                  </button>
                ))}
              </div>
            </div>
            
            {/* Indicator Selection */}
            <div>
              <h3 className="text-sm font-medium mb-2">Select Indicators (max 3)</h3>
              <div className="space-y-2">
                {availableIndicators.map(indicator => (
                  <label key={indicator.id} className="flex items-center space-x-2">
                    <input 
                      type="checkbox" 
                      checked={selectedIndicators.includes(indicator.id)}
                      onChange={() => toggleIndicator(indicator.id)}
                      className="rounded text-blue-600 focus:ring-blue-500"
                    />
                    <span className="text-sm">{indicator.name} ({indicator.category})</span>
                  </label>
                ))}
              </div>
            </div>
            
            {/* Geographic Filter */}
            {selectedView === 'regional' && (
              <div className="mt-4">
                <h3 className="text-sm font-medium mb-2">Geographic Filter</h3>
                <SomaliaMap 
                  selectedRegion={region} 
                  onRegionSelect={handleRegionSelect}
                  height="250px" 
                />
              </div>
            )}
          </CardContent>
        </Card>
        
        {/* Chart display */}
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Data Visualization</CardTitle>
            <CardDescription>
              {selectedView === 'time' 
                ? 'Time series data for selected indicators' 
                : 'Regional comparison for selected indicators'}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {selectedIndicators.length > 0 ? (
              renderChart()
            ) : (
              <div className="h-80 flex items-center justify-center text-gray-500">
                Please select at least one indicator
              </div>
            )}
          </CardContent>
        </Card>
      </div>
      
      {/* Data table */}
      <Card>
        <CardHeader>
          <CardTitle>Data Table</CardTitle>
          <CardDescription>
            Raw data for selected indicators
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-100 text-left">
                  <th className="p-2 border-b border-gray-200 text-gray-600 font-medium">
                    {selectedView === 'time' ? 'Year' : 'Region'}
                  </th>
                  {selectedIndicators.map(indicator => (
                    <th key={indicator} className="p-2 border-b border-gray-200 text-gray-600 font-medium">
                      {availableIndicators.find(i => i.id === indicator)?.name || indicator}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {getChartData().map((item, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="p-2 border-b border-gray-200 font-medium">
                      {selectedView === 'time' ? item.year : item.region}
                    </td>
                    {selectedIndicators.map(indicator => (
                      <td key={indicator} className="p-2 border-b border-gray-200">
                        {item[indicator]?.toString()}
                      </td>
                    ))}
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

export default DataExplorer
