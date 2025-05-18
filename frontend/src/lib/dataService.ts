import { useState, useEffect } from 'react';

// Types for our data models
export interface StatHighlight {
  label: string;
  value: string;
  change: string;
  trend: 'up' | 'down';
}

export interface PopulationData {
  year: string;
  population: number;
}

export interface GDPData {
  year: string;
  gdp: number;
}

export interface SectorData {
  name: string;
  value: number;
}

export interface LiveDataPoint {
  time: string;
  value: number;
}

export interface LiveDataUpdate {
  time: string;
  event: string;
  value: string;
}

// Simulate real-time data fetching with randomized changes
export const useStatHighlights = () => {
  const [data, setData] = useState<StatHighlight[]>([
    { label: 'Population', value: '16.3M', change: '+2.9%', trend: 'up' },
    { label: 'GDP Growth', value: '4.2%', change: '+0.5%', trend: 'up' },
    { label: 'Literacy Rate', value: '40%', change: '+5%', trend: 'up' },
    { label: 'Inflation', value: '6.1%', change: '-0.8%', trend: 'down' },
  ]);

  useEffect(() => {
    // Simulate periodic data updates
    const interval = setInterval(() => {
      setData(prev => {
        return prev.map(stat => {
          // Randomly decide if we should update this stat (20% chance)
          if (Math.random() > 0.8) {
            const isUp = Math.random() > 0.4; // 60% chance of being up
            const changeValue = parseFloat((Math.random() * 1.2).toFixed(1));
            
            return {
              ...stat,
              change: `${isUp ? '+' : '-'}${changeValue}%`,
              trend: isUp ? 'up' : 'down'
            };
          }
          return stat;
        });
      });
    }, 60000); // Update every minute

    return () => clearInterval(interval);
  }, []);

  return data;
};

export const usePopulationData = () => {
  const [data, setData] = useState<PopulationData[]>([
    { year: '2018', population: 14.7 },
    { year: '2019', population: 15.1 },
    { year: '2020', population: 15.4 },
    { year: '2021', population: 15.7 },
    { year: '2022', population: 16.0 },
    { year: '2023', population: 16.3 },
  ]);

  // In a real app, we would fetch this data from an API
  // For demo purposes, we'll just return the static data
  return data;
};

export const useGDPData = () => {
  const [data, setData] = useState<GDPData[]>([
    { year: '2018', gdp: 7.3 },
    { year: '2019', gdp: 7.5 },
    { year: '2020', gdp: 7.2 }, // Covid impact
    { year: '2021', gdp: 7.6 },
    { year: '2022', gdp: 7.9 },
    { year: '2023', gdp: 8.2 },
  ]);

  return data;
};

export const useSectorData = () => {
  const [data, setData] = useState<SectorData[]>([
    { name: 'Agriculture', value: 60 },
    { name: 'Services', value: 30 },
    { name: 'Industry', value: 10 },
  ]);

  return data;
};

// Hook for live data stream
export const useLiveDataStream = () => {
  const [liveData, setLiveData] = useState<LiveDataPoint[]>([
    { time: '00:00', value: 65 },
    { time: '02:00', value: 59 },
    { time: '04:00', value: 80 },
    { time: '06:00', value: 81 },
    { time: '08:00', value: 56 },
    { time: '10:00', value: 72 },
    { time: '12:00', value: 89 },
    { time: '14:00', value: 96 },
    { time: '16:00', value: 67 },
    { time: '18:00', value: 75 },
    { time: '20:00', value: 80 },
    { time: '22:00', value: 92 },
    { time: 'now', value: 87 },
  ]);

  useEffect(() => {
    const interval = setInterval(() => {
      setLiveData(prevData => {
        // Shift all values left
        const newData = [...prevData];
        
        // Remove first element
        newData.shift();
        
        // Generate a random value between 55-98
        const randomValue = Math.floor(Math.random() * 43) + 55;
        
        // Add new data point at the end
        newData.push({ time: 'now', value: randomValue });
        
        // Update timestamps
        return newData.map((point, index) => {
          if (index === newData.length - 1) return { time: 'now', value: point.value };
          return { time: point.time, value: point.value };
        });
      });
    }, 5000); // Update every 5 seconds
    
    return () => clearInterval(interval);
  }, []);

  return liveData;
};

// Live update notifications
export const useLiveUpdates = () => {
  const [updates, setUpdates] = useState<LiveDataUpdate[]>([
    { time: '14 min ago', event: 'Temperature data updated for Mogadishu', value: '28°C' },
    { time: '36 min ago', event: 'Rainfall data updated for Baidoa', value: '3.2mm' },
    { time: '1 hour ago', event: 'Agricultural yield report from Kismayo', value: '+4.5%' },
  ]);

  useEffect(() => {
    const interval = setInterval(() => {
      const events = [
        'Temperature data updated for Mogadishu',
        'Rainfall data updated for Baidoa',
        'Agricultural yield report from Kismayo',
        'Education enrollment in Hargeisa',
        'Healthcare access in Galmudug',
        'Fisheries output in Puntland',
        'Infrastructure development in Jubaland'
      ];
      
      const values = [
        '28°C', '29°C', '27°C', '3.2mm', '4.1mm', '+4.5%', '+2.8%', 
        '-1.5%', '+10.2%', '62%', '87%', '$2.4M', '+15K'
      ];
      
      const randomEvent = events[Math.floor(Math.random() * events.length)];
      const randomValue = values[Math.floor(Math.random() * values.length)];
      
      setUpdates(prev => {
        const newUpdates = [...prev];
        newUpdates.unshift({ 
          time: 'Just now', 
          event: randomEvent, 
          value: randomValue 
        });
        
        // Keep only the latest 3 updates
        return newUpdates.slice(0, 3);
      });
    }, 25000); // New update every 25 seconds
    
    return () => clearInterval(interval);
  }, []);

  return updates;
};

// Stock ticker data
export interface TickerItem {
  symbol: string;
  name: string;
  value: string;
  change: string;
  trend: 'up' | 'down';
}

export const useTickerData = () => {
  const [data, setData] = useState<TickerItem[]>([
    { symbol: 'GDP', name: 'GDP', value: '$8.2B', change: '+4.2%', trend: 'up' },
    { symbol: 'INFL', name: 'Inflation', value: '6.1%', change: '-0.8%', trend: 'down' },
    { symbol: 'UNEMP', name: 'Unemployment', value: '14.2%', change: '+0.2%', trend: 'up' },
    { symbol: 'FDI', name: 'Foreign Investment', value: '$412M', change: '+15.4%', trend: 'up' },
    { symbol: 'EXP', name: 'Exports', value: '$1.8B', change: '+7.1%', trend: 'up' },
    { symbol: 'LIT', name: 'Literacy Rate', value: '40%', change: '+5.0%', trend: 'up' },
  ]);

  useEffect(() => {
    const interval = setInterval(() => {
      setData(prev => {
        return prev.map(item => {
          // 30% chance to update each ticker item
          if (Math.random() > 0.7) {
            const isUp = Math.random() > 0.4;
            const changeValue = parseFloat((Math.random() * 2.5).toFixed(1));
            
            return {
              ...item,
              change: `${isUp ? '+' : '-'}${changeValue}%`,
              trend: isUp ? 'up' : 'down'
            };
          }
          return item;
        });
      });
    }, 12000); // Update ticker items every 12 seconds
    
    return () => clearInterval(interval);
  }, []);

  return data;
};

// Web scraping simulation (in a real app, this would be an API endpoint)
export const fetchLatestNews = async (): Promise<{title: string, date: string, tag: string}[]> => {
  // This would be a real API call in production
  // For demo purposes, we'll return mock data with random dates
  const news = [
    { title: 'Census Population Data Updated', tag: 'Demographics' },
    { title: 'Q1 2025 Economic Indicators Released', tag: 'Economics' },
    { title: 'Annual Education Statistics Report', tag: 'Education' },
    { title: 'Regional Development Indices', tag: 'Development' },
    { title: 'Healthcare Access Survey Results', tag: 'Healthcare' },
    { title: 'Agriculture Sector Growth Report', tag: 'Agriculture' },
    { title: 'Digital Inclusion Statistics Published', tag: 'Technology' },
    { title: 'Environmental Sustainability Metrics', tag: 'Environment' },
  ];
  
  // Simulate some network delay
  await new Promise(resolve => setTimeout(resolve, 500));
  
  // Generate random recent dates
  return news.map(item => {
    const daysAgo = Math.floor(Math.random() * 30) + 1;
    const date = new Date();
    date.setDate(date.getDate() - daysAgo);
    
    return {
      ...item,
      date: date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
    };
  }).slice(0, 4); // Return only 4 items
}; 