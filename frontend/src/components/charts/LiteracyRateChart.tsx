import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

// Mock data for literacy rates by region
const mockData = [
  { region: 'Banaadir', male: 78, female: 67 },
  { region: 'Jubaland', male: 61, female: 48 },
  { region: 'Puntland', male: 65, female: 53 },
  { region: 'Galmudug', male: 59, female: 43 },
  { region: 'Hirshabelle', male: 56, female: 41 },
  { region: 'South West', male: 58, female: 44 },
];

const LiteracyRateChart = () => {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Literacy Rate</CardTitle>
        <CardDescription>Literacy rate (%) by region and gender</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={mockData}
              margin={{
                top: 20,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="region" />
              <YAxis tickFormatter={(value) => `${value}%`} />
              <Tooltip formatter={(value) => [`${value}%`, 'Literacy Rate']} />
              <Legend />
              <Bar dataKey="male" name="Male" fill="#3182ce" />
              <Bar dataKey="female" name="Female" fill="#e53e3e" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
};

export default LiteracyRateChart;
