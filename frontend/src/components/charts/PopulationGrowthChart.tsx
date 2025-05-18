import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

// Mock data for Somalia population growth
const mockData = [
  { year: '2000', population: 7.4 },
  { year: '2005', population: 8.5 },
  { year: '2010', population: 9.8 },
  { year: '2015', population: 11.2 },
  { year: '2020', population: 12.9 },
  { year: '2025', population: 14.1 }, // Projected
];

const PopulationGrowthChart = () => {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Population Growth</CardTitle>
        <CardDescription>Somalia population growth trend (in millions)</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart
              data={mockData}
              margin={{
                top: 10,
                right: 30,
                left: 0,
                bottom: 0,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year" />
              <YAxis tickFormatter={(value) => `${value}M`} />
              <Tooltip formatter={(value) => [`${value}M`, 'Population']} />
              <Legend />
              <Area 
                type="monotone" 
                dataKey="population" 
                name="Population" 
                stroke="#3182ce" 
                fill="#3182ce" 
                fillOpacity={0.3} 
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
};

export default PopulationGrowthChart;
