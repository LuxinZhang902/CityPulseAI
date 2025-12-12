import React, { useEffect, useRef, useState } from 'react';
import { Loader } from '@googlemaps/js-api-loader';
import { Map as MapIcon, Layers } from 'lucide-react';

const GOOGLE_MAPS_API_KEY = process.env.REACT_APP_GOOGLE_MAPS_API_KEY || 'YOUR_API_KEY_HERE';

function MapView({ results }) {
  const mapRef = useRef(null);
  const googleMapRef = useRef(null);
  const markersRef = useRef([]);
  const heatmapRef = useRef(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  const [showHeatmap, setShowHeatmap] = useState(true);
  const [showMarkers, setShowMarkers] = useState(true);

  useEffect(() => {
    const loader = new Loader({
      apiKey: GOOGLE_MAPS_API_KEY,
      version: 'weekly',
      libraries: ['visualization', 'marker']
    });

    loader.load().then(() => {
      if (mapRef.current && !googleMapRef.current) {
        googleMapRef.current = new window.google.maps.Map(mapRef.current, {
          center: { lat: 37.7749, lng: -122.4194 },
          zoom: 12,
          styles: [
            {
              featureType: 'all',
              elementType: 'geometry',
              stylers: [{ color: '#1e293b' }]
            },
            {
              featureType: 'all',
              elementType: 'labels.text.fill',
              stylers: [{ color: '#cbd5e1' }]
            },
            {
              featureType: 'all',
              elementType: 'labels.text.stroke',
              stylers: [{ color: '#0f172a' }]
            },
            {
              featureType: 'water',
              elementType: 'geometry',
              stylers: [{ color: '#0f172a' }]
            },
            {
              featureType: 'road',
              elementType: 'geometry',
              stylers: [{ color: '#334155' }]
            }
          ],
          mapTypeControl: false,
          streetViewControl: false,
          fullscreenControl: true,
        });
        setMapLoaded(true);
      }
    });
  }, []);

  useEffect(() => {
    if (!mapLoaded || !googleMapRef.current || !results?.map_layers) {
      return;
    }

    clearMapLayers();

    const { heatmap, markers, center, zoom } = results.map_layers;

    if (center) {
      googleMapRef.current.setCenter(center);
    }
    if (zoom) {
      googleMapRef.current.setZoom(zoom);
    }

    if (showHeatmap && heatmap && heatmap.length > 0) {
      const heatmapData = heatmap.map(point => ({
        location: new window.google.maps.LatLng(point.lat, point.lng),
        weight: point.weight || 1
      }));

      heatmapRef.current = new window.google.maps.visualization.HeatmapLayer({
        data: heatmapData,
        map: googleMapRef.current,
        radius: 30,
        opacity: 0.7,
        gradient: [
          'rgba(0, 255, 255, 0)',
          'rgba(0, 255, 255, 1)',
          'rgba(0, 191, 255, 1)',
          'rgba(0, 127, 255, 1)',
          'rgba(0, 63, 255, 1)',
          'rgba(0, 0, 255, 1)',
          'rgba(0, 0, 223, 1)',
          'rgba(0, 0, 191, 1)',
          'rgba(0, 0, 159, 1)',
          'rgba(0, 0, 127, 1)',
          'rgba(63, 0, 91, 1)',
          'rgba(127, 0, 63, 1)',
          'rgba(191, 0, 31, 1)',
          'rgba(255, 0, 0, 1)'
        ]
      });
    }

    if (showMarkers && markers && markers.length > 0) {
      markers.forEach(markerData => {
        const severityColors = {
          critical: '#ef4444',
          high: '#f97316',
          medium: '#eab308',
          low: '#22c55e'
        };

        const marker = new window.google.maps.Marker({
          position: { lat: markerData.lat, lng: markerData.lng },
          map: googleMapRef.current,
          title: markerData.title,
          icon: {
            path: window.google.maps.SymbolPath.CIRCLE,
            scale: 8,
            fillColor: severityColors[markerData.severity] || severityColors.medium,
            fillOpacity: 0.8,
            strokeColor: '#ffffff',
            strokeWeight: 2
          }
        });

        const infoWindow = new window.google.maps.InfoWindow({
          content: `
            <div style="color: #1e293b; padding: 8px;">
              <h3 style="font-weight: bold; margin-bottom: 4px;">${markerData.title}</h3>
              <p style="font-size: 12px; margin: 0;">${markerData.description}</p>
              <p style="font-size: 11px; margin-top: 4px; color: #64748b;">
                Severity: <span style="color: ${severityColors[markerData.severity]}; font-weight: bold;">
                  ${markerData.severity.toUpperCase()}
                </span>
              </p>
            </div>
          `
        });

        marker.addListener('click', () => {
          infoWindow.open(googleMapRef.current, marker);
        });

        markersRef.current.push(marker);
      });
    }
  }, [results, mapLoaded, showHeatmap, showMarkers]);

  const clearMapLayers = () => {
    markersRef.current.forEach(marker => marker.setMap(null));
    markersRef.current = [];

    if (heatmapRef.current) {
      heatmapRef.current.setMap(null);
      heatmapRef.current = null;
    }
  };

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg overflow-hidden">
      <div className="p-4 border-b border-blue-500/20 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <MapIcon className="w-5 h-5 text-blue-400" />
          <h2 className="text-xl font-bold text-white">Crisis Map</h2>
        </div>
        
        {results && (
          <div className="flex items-center space-x-4">
            <button
              onClick={() => setShowHeatmap(!showHeatmap)}
              className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-sm transition-colors ${
                showHeatmap
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }`}
            >
              <Layers className="w-4 h-4" />
              <span>Heatmap</span>
            </button>
            <button
              onClick={() => setShowMarkers(!showMarkers)}
              className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-sm transition-colors ${
                showMarkers
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }`}
            >
              <MapIcon className="w-4 h-4" />
              <span>Markers</span>
            </button>
          </div>
        )}
      </div>

      <div className="relative" style={{ height: '600px' }}>
        <div ref={mapRef} className="w-full h-full" />
        
        {!mapLoaded && (
          <div className="absolute inset-0 flex items-center justify-center bg-slate-900/50">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
              <p className="text-slate-300">Loading map...</p>
            </div>
          </div>
        )}

        {!results && mapLoaded && (
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="bg-slate-800/90 backdrop-blur-sm border border-blue-500/30 rounded-lg p-6 text-center">
              <MapIcon className="w-12 h-12 text-blue-400 mx-auto mb-3" />
              <p className="text-slate-300">Ask a question to see crisis data on the map</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default MapView;
