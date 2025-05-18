import React, { useState, useEffect } from 'react';
import { useTheme } from '@/lib/themeContext';
import { useSomaliaRegionData, RegionData } from '@/lib/mapDataService';

// Props for the map component
interface SomaliaMapEnhancedProps {
  height: string;
  selectedRegion: string;
  onRegionSelect: (regionId: string) => void;
  dataCategory: 'literacy' | 'healthcare' | 'poverty' | 'population' | 'employment';
  year: string;
}

const SomaliaMapEnhanced: React.FC<SomaliaMapEnhancedProps> = ({
  height,
  selectedRegion = 'all',
  onRegionSelect,
  dataCategory = 'literacy',
  year = '2023',
}) => {
  const { theme } = useTheme();
  const [hoveredRegion, setHoveredRegion] = useState<string | null>(null);
  const [tooltipPos, setTooltipPos] = useState<{ x: number; y: number } | null>(null);
  
  // Use our real Somalia region data from the data service
  const { regionData } = useSomaliaRegionData(year);

  // Get color based on data value
  const getColor = (regionId: string): string => {
    if (selectedRegion !== 'all' && selectedRegion !== regionId) {
      return theme === 'dark' ? '#4B5563' : '#E5E7EB'; // Gray for unselected regions
    }

    const region = regionData.find(r => r.id === regionId);
    if (!region) return theme === 'dark' ? '#4B5563' : '#E5E7EB';

    let value: number;
    switch (dataCategory) {
      case 'literacy': value = region.literacy; break;
      case 'healthcare': value = region.healthcare; break;
      case 'poverty': value = region.poverty; break;
      case 'population': value = region.population * 10; break; // Scale for visualization
      case 'employment': value = region.employment; break;
      default: value = region.literacy;
    }

    // Different color scales for different data types
    if (dataCategory === 'poverty') {
      // Red scale for poverty (higher is worse)
      if (value > 65) return '#FCA5A5';
      if (value > 55) return '#F87171';
      if (value > 45) return '#EF4444';
      if (value > 35) return '#DC2626';
      return '#B91C1C';
    } else {
      // Blue scale for positive indicators (higher is better)
      if (value > 65) return '#3B82F6';
      if (value > 55) return '#60A5FA';
      if (value > 45) return '#93C5FD';
      if (value > 35) return '#BFDBFE';
      return '#DBEAFE';
    }
  };

  // Handle mouse events for the regions
  const handleMouseEnter = (regionId: string, event: React.MouseEvent) => {
    setHoveredRegion(regionId);
    // Position tooltip at mouse coordinates
    setTooltipPos({ x: event.clientX, y: event.clientY });
  };

  const handleMouseLeave = () => {
    setHoveredRegion(null);
    setTooltipPos(null);
  };

  const handleRegionClick = (regionId: string) => {
    onRegionSelect(regionId);
  };

  // Render tooltip for hovered region
  const renderTooltip = () => {
    if (!hoveredRegion || !tooltipPos) return null;

    const region = regionData.find(r => r.id === hoveredRegion);
    if (!region) return null;

    let displayValue: number | string;
    let unit: string;

    switch (dataCategory) {
      case 'literacy':
        displayValue = region.literacy.toFixed(1);
        unit = '%';
        break;
      case 'healthcare':
        displayValue = region.healthcare.toFixed(1);
        unit = '%';
        break;
      case 'poverty':
        displayValue = region.poverty.toFixed(1);
        unit = '%';
        break;
      case 'population':
        displayValue = region.population.toFixed(1);
        unit = 'M';
        break;
      case 'employment':
        displayValue = region.employment.toFixed(1);
        unit = '%';
        break;
      default:
        displayValue = region.literacy.toFixed(1);
        unit = '%';
    }

    return (
      <div 
        className={`absolute z-50 p-3 rounded-lg shadow-lg transform -translate-x-1/2 -translate-y-full pointer-events-none ${
          theme === 'dark' ? 'bg-gray-800 text-white' : 'bg-white text-gray-800'
        }`}
        style={{ 
          left: tooltipPos.x, 
          top: tooltipPos.y - 10,
          border: `1px solid ${theme === 'dark' ? '#4B5563' : '#E5E7EB'}`
        }}
      >
        <h3 className="font-bold text-sm">{region.name}</h3>
        <div className="text-xs mt-1 flex justify-between">
          <span className="text-gray-500 dark:text-gray-400">
            {dataCategory.charAt(0).toUpperCase() + dataCategory.slice(1)}:
          </span>
          <span className="font-medium ml-2">{displayValue}{unit}</span>
        </div>
        <div className="text-xs mt-1 flex justify-between">
          <span className="text-gray-500 dark:text-gray-400">Population:</span>
          <span className="font-medium ml-2">{region.population}M</span>
        </div>
      </div>
    );
  };

  return (
    <div className="relative w-full" style={{ height }}>
      {/* This is where the SVG map of Somalia will go */}
      <svg
        width="100%"
        height="100%"
        viewBox="0 0 800 600"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className={`transition-colors duration-300 ${
          theme === 'dark' ? 'bg-gray-900' : 'bg-gray-50'
        }`}
      >
        {/* Somaliland */}
        <path
          d="M200 150 L400 120 L480 180 L460 250 L320 280 L240 260 L200 150"
          fill={getColor('somaliland')}
          stroke={theme === 'dark' ? '#6B7280' : '#9CA3AF'}
          strokeWidth="2"
          onMouseEnter={(e) => handleMouseEnter('somaliland', e)}
          onMouseLeave={handleMouseLeave}
          onClick={() => handleRegionClick('somaliland')}
          className="cursor-pointer transition-colors duration-300 hover:opacity-80"
        />

        {/* Puntland */}
        <path
          d="M480 180 L600 140 L650 280 L580 380 L480 350 L460 250 L480 180"
          fill={getColor('puntland')}
          stroke={theme === 'dark' ? '#6B7280' : '#9CA3AF'}
          strokeWidth="2"
          onMouseEnter={(e) => handleMouseEnter('puntland', e)}
          onMouseLeave={handleMouseLeave}
          onClick={() => handleRegionClick('puntland')}
          className="cursor-pointer transition-colors duration-300 hover:opacity-80"
        />

        {/* Galmudug */}
        <path
          d="M460 250 L480 350 L420 450 L350 380 L320 280 L460 250"
          fill={getColor('galmudug')}
          stroke={theme === 'dark' ? '#6B7280' : '#9CA3AF'}
          strokeWidth="2"
          onMouseEnter={(e) => handleMouseEnter('galmudug', e)}
          onMouseLeave={handleMouseLeave}
          onClick={() => handleRegionClick('galmudug')}
          className="cursor-pointer transition-colors duration-300 hover:opacity-80"
        />

        {/* Hirshabelle */}
        <path
          d="M320 280 L350 380 L300 470 L230 440 L240 260 L320 280"
          fill={getColor('hirshabelle')}
          stroke={theme === 'dark' ? '#6B7280' : '#9CA3AF'}
          strokeWidth="2"
          onMouseEnter={(e) => handleMouseEnter('hirshabelle', e)}
          onMouseLeave={handleMouseLeave}
          onClick={() => handleRegionClick('hirshabelle')}
          className="cursor-pointer transition-colors duration-300 hover:opacity-80"
        />

        {/* Mogadishu */}
        <path
          d="M300 470 L350 480 L330 520 L280 510 L300 470"
          fill={getColor('mogadishu')}
          stroke={theme === 'dark' ? '#6B7280' : '#9CA3AF'}
          strokeWidth="2"
          onMouseEnter={(e) => handleMouseEnter('mogadishu', e)}
          onMouseLeave={handleMouseLeave}
          onClick={() => handleRegionClick('mogadishu')}
          className="cursor-pointer transition-colors duration-300 hover:opacity-80"
        />

        {/* Southwest State */}
        <path
          d="M230 440 L300 470 L280 510 L240 540 L180 520 L150 450 L230 440"
          fill={getColor('southwest')}
          stroke={theme === 'dark' ? '#6B7280' : '#9CA3AF'}
          strokeWidth="2"
          onMouseEnter={(e) => handleMouseEnter('southwest', e)}
          onMouseLeave={handleMouseLeave}
          onClick={() => handleRegionClick('southwest')}
          className="cursor-pointer transition-colors duration-300 hover:opacity-80"
        />

        {/* Jubaland */}
        <path
          d="M150 450 L180 520 L240 540 L270 580 L180 580 L120 520 L150 450"
          fill={getColor('jubaland')}
          stroke={theme === 'dark' ? '#6B7280' : '#9CA3AF'}
          strokeWidth="2"
          onMouseEnter={(e) => handleMouseEnter('jubaland', e)}
          onMouseLeave={handleMouseLeave}
          onClick={() => handleRegionClick('jubaland')}
          className="cursor-pointer transition-colors duration-300 hover:opacity-80"
        />

        {/* Ocean */}
        <text x="650" y="300" fill={theme === 'dark' ? '#9CA3AF' : '#4B5563'} fontSize="20">
          Indian Ocean
        </text>

        {/* Region labels */}
        {regionData.map(region => (
          <text
            key={region.id}
            x={region.coordinates[0] * 8} // Adjust coordinates to match SVG viewBox
            y={region.coordinates[1] * 40}
            fill={theme === 'dark' ? '#E5E7EB' : '#1F2937'}
            fontSize="12"
            fontWeight="500"
            textAnchor="middle"
            className="pointer-events-none"
          >
            {region.name}
          </text>
        ))}
      </svg>

      {/* Render tooltip */}
      {renderTooltip()}

      {/* Color legend */}
      <div className={`absolute bottom-4 right-4 p-3 rounded-lg ${
        theme === 'dark' ? 'bg-gray-800 text-white' : 'bg-white text-gray-800'
      } shadow-lg border ${theme === 'dark' ? 'border-gray-700' : 'border-gray-200'}`}>
        <div className="text-xs font-medium mb-2">
          {dataCategory.charAt(0).toUpperCase() + dataCategory.slice(1)} ({year})
        </div>
        <div className="flex items-center space-x-1">
          {dataCategory === 'poverty' ? (
            <>
              <div className="w-4 h-4 bg-[#B91C1C]"></div>
              <div className="w-4 h-4 bg-[#DC2626]"></div>
              <div className="w-4 h-4 bg-[#EF4444]"></div>
              <div className="w-4 h-4 bg-[#F87171]"></div>
              <div className="w-4 h-4 bg-[#FCA5A5]"></div>
              <div className="flex justify-between w-full text-[10px] px-1">
                <span>Low</span>
                <span>High</span>
              </div>
            </>
          ) : (
            <>
              <div className="w-4 h-4 bg-[#DBEAFE]"></div>
              <div className="w-4 h-4 bg-[#BFDBFE]"></div>
              <div className="w-4 h-4 bg-[#93C5FD]"></div>
              <div className="w-4 h-4 bg-[#60A5FA]"></div>
              <div className="w-4 h-4 bg-[#3B82F6]"></div>
              <div className="flex justify-between w-full text-[10px] px-1">
                <span>Low</span>
                <span>High</span>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default SomaliaMapEnhanced; 