import React from 'react';
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Legend,
  ResponsiveContainer,
  Tooltip
} from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

// Mock data for vaccination coverage by region
const mockData = [
  { vaccine: 'BCG', coverage: 85 },
  { vaccine: 'DTP3', coverage: 72 },
  { vaccine: 'Polio', coverage: 78 },
  { vaccine: 'Measles', coverage: 68 },
  { vaccine: 'PCV', coverage: 62 },
  { vaccine: 'Rotavirus', coverage: 55 },
];

const VaccinationCoverageChart = () => {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Vaccination Coverage</CardTitle>
        <CardDescription>Childhood vaccination coverage rates (%)</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart cx="50%" cy="50%" outerRadius="80%" data={mockData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="vaccine" />
              <PolarRadiusAxis angle={30} domain={[0, 100]} />
              <Radar
                name="Vaccination Coverage"
                dataKey="coverage"
                stroke="#38a169"
                fill="#38a169"
                fillOpacity={0.5}
              />
              <Tooltip formatter={(value) => `${value}%`} />
              <Legend />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
};

export default VaccinationCoverageChart;
