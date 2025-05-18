import React from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';

// Mock data for key statistical indicators
const mockKeyIndicators = [
  {
    id: 1,
    category: 'Demographics',
    indicator: 'Total Population',
    value: '12.9 million',
    year: 2020,
    change: '+2.5%',
    trend: 'increasing'
  },
  {
    id: 2,
    category: 'Demographics',
    indicator: 'Urban Population',
    value: '45.6%',
    year: 2020,
    change: '+1.2%',
    trend: 'increasing'
  },
  {
    id: 3,
    category: 'Economy',
    indicator: 'GDP',
    value: '$4.72 billion',
    year: 2019,
    change: '+2.9%',
    trend: 'increasing'
  },
  {
    id: 4,
    category: 'Economy',
    indicator: 'Inflation Rate',
    value: '4.1%',
    year: 2020,
    change: '-0.3%',
    trend: 'decreasing'
  },
  {
    id: 5,
    category: 'Education',
    indicator: 'Literacy Rate',
    value: '58.3%',
    year: 2020,
    change: '+2.4%',
    trend: 'increasing'
  },
  {
    id: 6,
    category: 'Health',
    indicator: 'Life Expectancy',
    value: '57.2 years',
    year: 2020,
    change: '+0.8',
    trend: 'increasing'
  },
  {
    id: 7,
    category: 'Health',
    indicator: 'Infant Mortality',
    value: '72/1,000',
    year: 2020,
    change: '-3.4',
    trend: 'decreasing'
  },
  {
    id: 8,
    category: 'Infrastructure',
    indicator: 'Access to Electricity',
    value: '32.6%',
    year: 2019,
    change: '+2.8%',
    trend: 'increasing'
  }
];

interface KeyIndicatorsTableProps {
  filteredRegion?: string;
  filteredSector?: string;
}

const KeyIndicatorsTable = ({ filteredRegion, filteredSector }: KeyIndicatorsTableProps) => {
  // Filter indicators based on region and sector (in a real app, this would be done via API)
  // For this mock, we'll just return all indicators
  const indicators = mockKeyIndicators;

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Key Statistical Indicators</CardTitle>
        <CardDescription>
          {filteredRegion && filteredRegion !== 'all' 
            ? `Showing indicators for ${filteredRegion} region` 
            : 'Showing national indicators'}
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
              {indicators.map((indicator) => (
                <tr key={indicator.id} className="hover:bg-gray-50">
                  <td className="p-2 border-b border-gray-200">{indicator.category}</td>
                  <td className="p-2 border-b border-gray-200 font-medium">{indicator.indicator}</td>
                  <td className="p-2 border-b border-gray-200">{indicator.value}</td>
                  <td className="p-2 border-b border-gray-200">{indicator.year}</td>
                  <td className="p-2 border-b border-gray-200">
                    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${indicator.trend === 'increasing' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
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
  );
};

export default KeyIndicatorsTable;
