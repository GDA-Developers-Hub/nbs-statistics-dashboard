import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { useTheme } from '@/lib/themeContext';
import SomaliaMapEnhanced from '@/components/map/SomaliaMapEnhanced';
import { useSomaliaRegionData, getDataInsights } from '@/lib/mapDataService';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface MapDashboardProps {
  className?: string;
}

const MapDashboard: React.FC<MapDashboardProps> = ({ className = '' }) => {
  const { theme } = useTheme();
  const [selectedRegion, setSelectedRegion] = useState('all');
  const [dataCategory, setDataCategory] = useState<'literacy' | 'healthcare' | 'poverty' | 'population' | 'employment'>('literacy');
  const [year, setYear] = useState('2023');
  
  // Use our real Somalia region data from the data service
  const { regionData, years } = useSomaliaRegionData(year);
  
  // Process data for charts based on current selection
  const getChartData = () => {
    // Filter by selected region if not "all"
    const filteredData = selectedRegion === 'all' 
      ? regionData 
      : regionData.filter(item => item.id === selectedRegion);
    
    return filteredData.map(region => ({
      name: region.name,
      value: region[dataCategory]
    }));
  };
  
  // Dynamic title based on selection
  const getDashboardTitle = () => {
    const regionText = selectedRegion === 'all' ? 'Somalia' : regionData.find(r => r.id === selectedRegion)?.name || 'Somalia';
    const categoryText = dataCategory.charAt(0).toUpperCase() + dataCategory.slice(1);
    
    return `${categoryText} Data for ${regionText} (${year})`;
  };
  
  // Labels and descriptions for data categories
  const categoryInfo = {
    literacy: {
      title: 'Literacy Rate',
      description: 'Percentage of population age 15+ who can read and write',
      unit: '%',
    },
    healthcare: {
      title: 'Healthcare Access',
      description: 'Percentage of population with access to basic healthcare services',
      unit: '%',
    },
    poverty: {
      title: 'Poverty Rate',
      description: 'Percentage of population living below the poverty line',
      unit: '%',
    },
    population: {
      title: 'Population',
      description: 'Total population in millions',
      unit: 'M',
    },
    employment: {
      title: 'Employment Rate',
      description: 'Percentage of working-age population that is employed',
      unit: '%',
    },
  };
  
  // Get insights based on the current selection
  const insights = getDataInsights(dataCategory, year);
  
  return (
    <div className={`w-full rounded-xl border ${
      theme === 'dark' ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'
    } shadow-lg overflow-hidden ${className}`}>
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <h2 className="text-xl font-semibold text-gray-800 dark:text-white">{getDashboardTitle()}</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          {categoryInfo[dataCategory].description}
        </p>
      </div>
      
      {/* Filter Controls */}
      <div className="p-4 bg-gray-50 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 flex flex-wrap gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Data Category</label>
          <div className="flex flex-wrap gap-2">
            {Object.keys(categoryInfo).map((category) => (
              <Button
                key={category}
                variant={dataCategory === category ? "default" : "outline"}
                size="sm"
                onClick={() => setDataCategory(category as any)}
                className="capitalize"
              >
                {categoryInfo[category as keyof typeof categoryInfo].title}
              </Button>
            ))}
          </div>
        </div>
        
        <div className="ml-auto">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Year</label>
          <div className="flex gap-2">
            {years.map((y) => (
              <Button
                key={y}
                variant={year === y ? "default" : "outline"}
                size="sm"
                onClick={() => setYear(y)}
              >
                {y}
              </Button>
            ))}
          </div>
        </div>
      </div>
      
      {/* Map and Chart Container */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 p-4">
        {/* Map */}
        <div className="lg:col-span-2 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700">
          <SomaliaMapEnhanced
            height="500px"
            selectedRegion={selectedRegion}
            onRegionSelect={setSelectedRegion}
            dataCategory={dataCategory}
            year={year}
          />
        </div>
        
        {/* Statistics */}
        <div className="flex flex-col">
          <div className={`p-4 rounded-lg border ${
            theme === 'dark' ? 'bg-gray-900 border-gray-700' : 'bg-gray-50 border-gray-200'
          } mb-4`}>
            <h3 className="text-lg font-medium mb-2 text-gray-700 dark:text-gray-200">
              {categoryInfo[dataCategory].title} by Region
            </h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={getChartData()}
                  layout="vertical"
                  margin={{ top: 5, right: 30, left: 60, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} stroke={theme === 'dark' ? '#374151' : '#E5E7EB'} />
                  <XAxis 
                    type="number"
                    stroke={theme === 'dark' ? '#9CA3AF' : '#6B7280'}
                    domain={[0, dataCategory === 'population' ? 5 : 100]} 
                  />
                  <YAxis 
                    dataKey="name" 
                    type="category" 
                    width={80}
                    stroke={theme === 'dark' ? '#9CA3AF' : '#6B7280'}
                  />
                  <Tooltip
                    contentStyle={{ 
                      backgroundColor: theme === 'dark' ? 'rgba(17, 24, 39, 0.9)' : 'rgba(255, 255, 255, 0.9)',
                      color: theme === 'dark' ? '#E5E7EB' : 'inherit',
                      borderRadius: '0.375rem',
                      border: theme === 'dark' ? '1px solid #374151' : '1px solid #E5E7EB',
                    }}
                    formatter={(value: number) => [`${value.toFixed(1)}${categoryInfo[dataCategory].unit}`, categoryInfo[dataCategory].title]}
                  />
                  <Bar 
                    dataKey="value" 
                    fill={dataCategory === 'poverty' ? '#EF4444' : '#3B82F6'} 
                    radius={[0, 4, 4, 0]}
                    barSize={20}
                    animationDuration={1000}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
          
          {/* Key Insights */}
          <motion.div 
            className={`p-4 rounded-lg border ${
              theme === 'dark' ? 'bg-gray-900 border-gray-700' : 'bg-gray-50 border-gray-200'
            }`}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
            key={`${selectedRegion}-${dataCategory}-${year}`} // Force re-render on selection change
          >
            <h3 className="text-lg font-medium mb-2 text-gray-700 dark:text-gray-200">Key Insights</h3>
            <ul className="space-y-2 text-sm">
              {insights.map((insight, index) => (
                <li key={index} className="flex items-start">
                  <span className={`h-5 w-5 rounded-full ${
                    dataCategory === 'poverty'
                      ? 'bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-400'
                      : 'bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400'
                  } flex items-center justify-center text-xs mr-2 mt-0.5`}>{insight.icon}</span>
                  <span className="text-gray-600 dark:text-gray-300">{insight.text}</span>
                </li>
              ))}
            </ul>
          </motion.div>
        </div>
      </div>
      
      {/* Action buttons */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-700 flex justify-between">
        <Button
          variant="outline"
          size="sm"
          onClick={() => {
            setSelectedRegion('all');
            setDataCategory('literacy');
            setYear('2023');
          }}
        >
          Reset View
        </Button>
        
        <Button size="sm">
          Export Data
        </Button>
      </div>
    </div>
  );
};

export default MapDashboard; 