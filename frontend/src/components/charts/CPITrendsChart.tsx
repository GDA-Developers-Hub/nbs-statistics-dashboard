import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

// Mock data for CPI trends
const mockData = [
  { month: 'Jan', food: 112.4, housing: 108.2, overall: 110.1 },
  { month: 'Feb', food: 113.1, housing: 108.5, overall: 111.0 },
  { month: 'Mar', food: 114.6, housing: 109.0, overall: 112.3 },
  { month: 'Apr', food: 115.8, housing: 109.8, overall: 113.5 },
  { month: 'May', food: 117.2, housing: 110.2, overall: 114.7 },
  { month: 'Jun', food: 118.5, housing: 110.8, overall: 115.9 },
  { month: 'Jul', food: 119.3, housing: 111.5, overall: 116.8 },
  { month: 'Aug', food: 119.1, housing: 112.0, overall: 116.5 },
  { month: 'Sep', food: 118.5, housing: 112.3, overall: 116.0 },
  { month: 'Oct', food: 117.9, housing: 112.7, overall: 115.6 },
  { month: 'Nov', food: 118.2, housing: 113.0, overall: 116.1 },
  { month: 'Dec', food: 119.1, housing: 113.5, overall: 117.0 },
];

const CPITrendsChart = () => {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>CPI Trends</CardTitle>
        <CardDescription>Consumer Price Index trends (2020 = 100)</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={mockData}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis domain={[100, 120]} />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="overall"
                name="Overall CPI"
                stroke="#3182ce"
                activeDot={{ r: 8 }}
                strokeWidth={2}
              />
              <Line 
                type="monotone" 
                dataKey="food" 
                name="Food" 
                stroke="#e53e3e" 
              />
              <Line 
                type="monotone" 
                dataKey="housing" 
                name="Housing" 
                stroke="#38a169" 
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
};

export default CPITrendsChart;
