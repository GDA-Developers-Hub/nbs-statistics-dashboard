import { useEffect, useRef, useState } from 'react'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

// Set Mapbox access token
mapboxgl.accessToken = 'pk.eyJ1IjoiZ2RhLTIwMjUiLCJhIjoiY21hdG1mamQ0MDRsaDJrczVseTZtNnQwOSJ9.1LUb87KeBA1EUxagi3U9Ng'

// Define the GeoJSON type
interface GeoJSONFeature {
  type: string
  properties: {
    name: string
    code: string
    [key: string]: any
  }
  geometry: {
    type: string
    coordinates: any
  }
}

interface GeoJSONData {
  type: string
  features: GeoJSONFeature[]
}

// Sample GeoJSON data (simplified version for Somalia regions)
// In a real application, this would be loaded from an API
const somaliaGeoJSON: GeoJSONData = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      properties: {
        name: 'Banaadir',
        code: 'banadir',
        capital: 'Mogadishu'
      },
      geometry: {
        type: 'Polygon',
        coordinates: [[[45.3, 2.0], [45.4, 2.0], [45.4, 2.1], [45.3, 2.1], [45.3, 2.0]]]
      }
    },
    {
      type: 'Feature',
      properties: {
        name: 'Jubaland',
        code: 'jubaland',
        capital: 'Kismayo'
      },
      geometry: {
        type: 'Polygon',
        coordinates: [[[41.5, 0.0], [43.0, 0.0], [43.0, 3.0], [41.5, 3.0], [41.5, 0.0]]]
      }
    },
    {
      type: 'Feature',
      properties: {
        name: 'Puntland',
        code: 'puntland',
        capital: 'Garowe'
      },
      geometry: {
        type: 'Polygon',
        coordinates: [[[47.0, 7.0], [49.5, 7.0], [49.5, 11.0], [47.0, 11.0], [47.0, 7.0]]]
      }
    },
    {
      type: 'Feature',
      properties: {
        name: 'Galmudug',
        code: 'galmudug',
        capital: 'Dhusamareb'
      },
      geometry: {
        type: 'Polygon',
        coordinates: [[[45.0, 4.0], [47.0, 4.0], [47.0, 7.0], [45.0, 7.0], [45.0, 4.0]]]
      }
    },
    {
      type: 'Feature',
      properties: {
        name: 'Hirshabelle',
        code: 'hirshabelle',
        capital: 'Jowhar'
      },
      geometry: {
        type: 'Polygon',
        coordinates: [[[44.0, 2.0], [46.0, 2.0], [46.0, 4.0], [44.0, 4.0], [44.0, 2.0]]]
      }
    },
    {
      type: 'Feature',
      properties: {
        name: 'South West',
        code: 'southwest',
        capital: 'Baidoa'
      },
      geometry: {
        type: 'Polygon',
        coordinates: [[[42.0, 1.0], [44.0, 1.0], [44.0, 3.0], [42.0, 3.0], [42.0, 1.0]]]
      }
    }
  ]
}

interface SomaliaMapProps {
  selectedRegion: string
  onRegionSelect: (regionCode: string) => void
  height?: string
}

const SomaliaMap = ({ selectedRegion = 'all', onRegionSelect, height = '400px' }: SomaliaMapProps) => {
  const mapRef = useRef<HTMLDivElement>(null)
  const [map, setMap] = useState<mapboxgl.Map | null>(null)
  const [hoveredRegionId, setHoveredRegionId] = useState<string | null>(null)
  
  // Initialize the map
  useEffect(() => {
    if (mapRef.current && !map) {
      // Create the map instance
      const mapInstance = new mapboxgl.Map({
        container: mapRef.current,
        style: 'mapbox://styles/mapbox/light-v11', // Light base map style
        center: [46.199616, 5.152149], // Somalia center coordinates (reversed order for Mapbox)
        zoom: 4.5,
        attributionControl: true
      })

      // Add navigation controls
      mapInstance.addControl(new mapboxgl.NavigationControl(), 'top-right')
      
      // Save map instance to state
      setMap(mapInstance)
      
      // Wait for map to load before adding data
      mapInstance.on('load', () => {
        // Add source for Somalia regions
        mapInstance.addSource('somalia-regions', {
          type: 'geojson',
          data: somaliaGeoJSON as any
        })
        
        // Add fill layer for regions
        mapInstance.addLayer({
          id: 'somalia-regions-fill',
          type: 'fill',
          source: 'somalia-regions',
          layout: {},
          paint: {
            'fill-color': [
              'case',
              ['==', ['get', 'code'], selectedRegion], '#3182ce', // Selected region color
              ['==', ['get', 'code'], hoveredRegionId], '#90cdf4', // Hovered region color
              '#60a5fa' // Default color
            ],
            'fill-opacity': [
              'case',
              ['==', ['get', 'code'], selectedRegion], 0.7, // Selected region opacity
              ['==', ['get', 'code'], hoveredRegionId], 0.6, // Hovered region opacity
              0.4 // Default opacity
            ]
          }
        })
        
        // Add line layer for region borders
        mapInstance.addLayer({
          id: 'somalia-regions-line',
          type: 'line',
          source: 'somalia-regions',
          layout: {},
          paint: {
            'line-color': '#ffffff',
            'line-width': 1.5
          }
        })
        
        // Add region labels
        mapInstance.addLayer({
          id: 'somalia-regions-label',
          type: 'symbol',
          source: 'somalia-regions',
          layout: {
            'text-field': ['get', 'name'],
            'text-size': 12,
            'text-anchor': 'center',
            'text-justify': 'center'
          },
          paint: {
            'text-color': '#333',
            'text-halo-color': '#fff',
            'text-halo-width': 1
          }
        })
        
        // Add hover interactivity
        mapInstance.on('mousemove', 'somalia-regions-fill', (e) => {
          if (e.features && e.features.length > 0) {
            const feature = e.features[0];
            const regionCode = feature.properties.code;
            
            // Change cursor to pointer and update hovered region
            mapInstance.getCanvas().style.cursor = 'pointer';
            setHoveredRegionId(regionCode);
            
            // Show tooltip (requires custom implementation)
            // We could add a custom tooltip here if needed
          }
        })
        
        // Reset on mouse leave
        mapInstance.on('mouseleave', 'somalia-regions-fill', () => {
          mapInstance.getCanvas().style.cursor = '';
          setHoveredRegionId(null);
        })
        
        // Add click handler
        mapInstance.on('click', 'somalia-regions-fill', (e) => {
          if (e.features && e.features.length > 0) {
            const feature = e.features[0];
            const regionCode = feature.properties.code;
            onRegionSelect(regionCode);
          }
        })
      })
    }

    // Cleanup on unmount
    return () => {
      if (map) {
        map.remove();
        setMap(null);
      }
    }
  }, [mapRef])
  
  // Update map when selected region changes
  useEffect(() => {
    if (map && map.isStyleLoaded() && map.getSource('somalia-regions')) {
      // Update the fill layer to reflect the new selected region
      map.setPaintProperty('somalia-regions-fill', 'fill-color', [
        'case',
        ['==', ['get', 'code'], selectedRegion], '#3182ce', // Selected region color
        ['==', ['get', 'code'], hoveredRegionId], '#90cdf4', // Hovered region color
        '#60a5fa' // Default color
      ])
      
      map.setPaintProperty('somalia-regions-fill', 'fill-opacity', [
        'case',
        ['==', ['get', 'code'], selectedRegion], 0.7, // Selected region opacity
        ['==', ['get', 'code'], hoveredRegionId], 0.6, // Hovered region opacity
        0.4 // Default opacity
      ])
      
      // If a specific region is selected, zoom to it
      if (selectedRegion !== 'all') {
        // Find the selected feature
        const selectedFeature = somaliaGeoJSON.features.find(
          feature => feature.properties.code === selectedRegion
        )
        
        if (selectedFeature) {
          // Simple calculation for bounding box (for more complex geometries, a proper bbox calculation would be better)
          const coordinates = selectedFeature.geometry.coordinates[0];
          let minLng = Infinity, maxLng = -Infinity, minLat = Infinity, maxLat = -Infinity;
          
          for (const [lng, lat] of coordinates) {
            minLng = Math.min(minLng, lng);
            maxLng = Math.max(maxLng, lng);
            minLat = Math.min(minLat, lat);
            maxLat = Math.max(maxLat, lat);
          }
          
          // Fit bounds with padding
          map.fitBounds([
            [minLng, minLat], // Southwest coordinates
            [maxLng, maxLat]  // Northeast coordinates
          ], {
            padding: 50,
            duration: 1000
          });
        }
      } else {
        // Zoom out to see all of Somalia
        map.flyTo({
          center: [46.199616, 5.152149],
          zoom: 4.5,
          duration: 1000
        });
      }
    }
  }, [selectedRegion, hoveredRegionId, map])

  return (
    <div className="rounded-lg border border-gray-200 bg-white shadow-sm">
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-medium text-gray-900">Geographic Filter</h3>
        <p className="text-sm text-gray-500">Click on a region to filter data</p>
      </div>
      <div 
        ref={mapRef} 
        style={{ height, width: '100%' }}
        className="leaflet-container"
      />
      <div className="p-3 border-t border-gray-200 text-xs text-gray-500">
        {selectedRegion === 'all' ? 'Showing all regions' : `Selected: ${somaliaGeoJSON.features.find(f => f.properties.code === selectedRegion)?.properties.name || ''}`}
      </div>
    </div>
  )
}

export default SomaliaMap
