import React, { useState } from 'react';
import { AlertCircle, Activity, MapPin, Database } from 'lucide-react';
import QueryPanel from './components/QueryPanel';
import MapView from './components/MapView';
import ResultsPanel from './components/ResultsPanel';
import { analyzeQuery } from './services/api';

function App() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleQuery = async (question) => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await analyzeQuery(question);
      setResults(data);
    } catch (err) {
      setError(err.message || 'Failed to analyze query');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <header className="bg-slate-900/80 backdrop-blur-sm border-b border-blue-500/20">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Activity className="w-8 h-8 text-blue-400" />
              <div>
                <h1 className="text-2xl font-bold text-white">CityPulse AI</h1>
                <p className="text-sm text-blue-300">Real-Time Urban Crisis Intelligence</p>
              </div>
            </div>
            <div className="flex items-center space-x-4 text-sm text-slate-300">
              <div className="flex items-center space-x-2">
                <Database className="w-4 h-4" />
                <span>Live SQLite</span>
              </div>
              <div className="flex items-center space-x-2">
                <MapPin className="w-4 h-4" />
                <span>San Francisco</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1 space-y-6">
            <QueryPanel onQuery={handleQuery} loading={loading} />
            {error && (
              <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-4">
                <div className="flex items-start space-x-3">
                  <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                  <div>
                    <h3 className="text-red-400 font-semibold">Error</h3>
                    <p className="text-red-300 text-sm mt-1">{error}</p>
                  </div>
                </div>
              </div>
            )}
            {results && <ResultsPanel results={results} />}
          </div>

          <div className="lg:col-span-2">
            <MapView results={results} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
