import React from 'react';
import { Map as MapIcon, MapPin, AlertCircle } from 'lucide-react';

/**
 * Simplified MapView - Works without Google Maps API
 * Shows location data in a list format instead of an interactive map
 * 
 * To use this version:
 * 1. Rename this file to MapView.js (backup the original first)
 * 2. Or get a Google Maps API key and use the full version
 */

function MapView({ results }) {
  if (!results?.map_layers) {
    return (
      <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg overflow-hidden">
        <div className="p-4 border-b border-blue-500/20 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <MapIcon className="w-5 h-5 text-blue-400" />
            <h2 className="text-xl font-bold text-white">Location Data</h2>
          </div>
        </div>
        
        <div className="p-8 text-center">
          <div className="bg-slate-900/50 border border-slate-700 rounded-lg p-8">
            <MapIcon className="w-16 h-16 text-slate-500 mx-auto mb-4" />
            <p className="text-slate-400">Ask a question to see location data</p>
          </div>
        </div>
      </div>
    );
  }

  const { markers, center } = results.map_layers;

  const getSeverityColor = (severity) => {
    const colors = {
      critical: 'bg-red-500 text-red-100 border-red-600',
      high: 'bg-orange-500 text-orange-100 border-orange-600',
      medium: 'bg-yellow-500 text-yellow-100 border-yellow-600',
      low: 'bg-green-500 text-green-100 border-green-600'
    };
    return colors[severity] || colors.medium;
  };

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg overflow-hidden">
      <div className="p-4 border-b border-blue-500/20 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <MapIcon className="w-5 h-5 text-blue-400" />
          <h2 className="text-xl font-bold text-white">Location Data</h2>
        </div>
        <div className="flex items-center space-x-2 text-sm text-yellow-400">
          <AlertCircle className="w-4 h-4" />
          <span>Map view requires Google Maps API key</span>
        </div>
      </div>

      <div className="p-6">
        {/* Center coordinates */}
        {center && (
          <div className="mb-6 bg-slate-900/50 border border-slate-700 rounded-lg p-4">
            <h3 className="text-sm font-semibold text-slate-400 mb-2">Map Center</h3>
            <div className="text-white font-mono text-sm">
              {center.lat.toFixed(4)}, {center.lng.toFixed(4)}
            </div>
          </div>
        )}

        {/* Markers list */}
        {markers && markers.length > 0 ? (
          <div>
            <h3 className="text-sm font-semibold text-slate-400 mb-3">
              Locations ({markers.length})
            </h3>
            <div className="space-y-3 max-h-[500px] overflow-y-auto">
              {markers.map((marker, index) => (
                <div
                  key={index}
                  className="bg-slate-900/50 border border-slate-700 rounded-lg p-4 hover:border-blue-500/50 transition-colors"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <MapPin className="w-4 h-4 text-blue-400 flex-shrink-0" />
                      <h4 className="text-white font-semibold">{marker.title}</h4>
                    </div>
                    <span className={`px-2 py-1 rounded text-xs font-semibold border ${getSeverityColor(marker.severity)}`}>
                      {marker.severity.toUpperCase()}
                    </span>
                  </div>
                  
                  <p className="text-slate-300 text-sm mb-2">{marker.description}</p>
                  
                  <div className="flex items-center space-x-4 text-xs text-slate-400 font-mono">
                    <span>Lat: {marker.lat.toFixed(4)}</span>
                    <span>Lng: {marker.lng.toFixed(4)}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="text-center py-8 text-slate-400">
            No location markers available
          </div>
        )}

        {/* Instructions */}
        <div className="mt-6 bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
          <h4 className="text-blue-400 font-semibold mb-2 flex items-center space-x-2">
            <AlertCircle className="w-4 h-4" />
            <span>Want to see an interactive map?</span>
          </h4>
          <p className="text-blue-200 text-sm">
            Get a free Google Maps API key and add it to <code className="bg-slate-900 px-1 py-0.5 rounded">/frontend/.env</code>
          </p>
          <p className="text-blue-300 text-xs mt-2">
            See <code className="bg-slate-900 px-1 py-0.5 rounded">GOOGLE_MAPS_SETUP.md</code> for instructions
          </p>
        </div>
      </div>
    </div>
  );
}

export default MapView;
