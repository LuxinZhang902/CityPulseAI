import React, { useState } from 'react';
import MapView from './components/MapView';
import QueryPanel from './components/QueryPanel';
import ResultsPanel from './components/ResultsPanel';
import ChartsPanel from './components/ChartsPanel';
import { Brain, BarChart3, Map, Database, Sparkles, Loader, Activity, MapPin, AlertCircle } from 'lucide-react';
import { analyzeQuery } from './services/api';

function App() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [activeView, setActiveView] = useState('split'); // 'split', 'map', 'data'

  const handleQuery = async (question) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();
      
      if (data.error) {
        setError(data.error);
      } else {
        setResults(data);
      }
    } catch (err) {
      setError('Failed to connect to the server. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!results) return;
    
    try {
      const response = await fetch('http://localhost:8000/api/generate-pdf', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: results.query }),
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `citypulse-report-${new Date().toISOString().split('T')[0]}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        console.error('Failed to generate PDF');
      }
    } catch (err) {
      console.error('Error downloading PDF:', err);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Modern Header */}
      <header className="bg-slate-900/90 backdrop-blur-md border-b border-blue-500/20 shadow-2xl">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="relative">
                <Activity className="w-10 h-10 text-blue-400" />
                <Sparkles className="w-4 h-4 text-yellow-400 absolute -top-1 -right-1 animate-pulse" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-white bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                  CityPulse AI
                </h1>
                <p className="text-sm text-blue-300">Real-Time Urban Crisis Intelligence</p>
              </div>
            </div>
            
            {/* View Toggle Buttons */}
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-4 text-sm text-slate-300">
                <div className="flex items-center space-x-2">
                  <Database className="w-4 h-4 text-green-400" />
                  <span>Live SQLite</span>
                </div>
                <div className="flex items-center space-x-2">
                  <MapPin className="w-4 h-4 text-red-400" />
                  <span>San Francisco</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Brain className="w-4 h-4 text-purple-400" />
                  <span>SnowLeopard AI</span>
                </div>
              </div>
              
              {/* View Mode Selector */}
              <div className="flex bg-slate-800/50 rounded-lg p-1 border border-slate-700">
                <button
                  onClick={() => setActiveView('split')}
                  className={`px-3 py-1 rounded text-sm font-medium transition-all ${
                    activeView === 'split' 
                      ? 'bg-blue-600 text-white' 
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  Split
                </button>
                <button
                  onClick={() => setActiveView('map')}
                  className={`px-3 py-1 rounded text-sm font-medium transition-all ${
                    activeView === 'map' 
                      ? 'bg-blue-600 text-white' 
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  Map
                </button>
                <button
                  onClick={() => setActiveView('data')}
                  className={`px-3 py-1 rounded text-sm font-medium transition-all ${
                    activeView === 'data' 
                      ? 'bg-blue-600 text-white' 
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  Data
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="container mx-auto px-4 py-6">
        {/* Error Display */}
        {error && (
          <div className="mb-6 bg-red-500/10 border border-red-500/50 rounded-lg p-4 backdrop-blur-sm">
            <div className="flex items-start space-x-3">
              <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="text-red-400 font-semibold">Error</h3>
                <p className="text-red-300 text-sm mt-1">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Loading State - Inline */}
        {loading && (
          <div className="mb-6 bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-12">
            <div className="flex flex-col items-center space-y-6">
              <div className="relative">
                <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-400"></div>
                <Brain className="w-8 h-8 text-blue-400 absolute inset-0 m-auto" />
              </div>
              <div className="text-center">
                <p className="text-white text-xl font-semibold">Analyzing with SnowLeopard AI</p>
                <p className="text-slate-400 text-sm mt-2">Processing your query...</p>
                <div className="flex items-center justify-center space-x-2 mt-4">
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse" style={{animationDelay: '0.2s'}}></div>
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse" style={{animationDelay: '0.4s'}}></div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Dynamic Layout Based on View */}
        {activeView === 'split' && (
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
            {/* Left Panel - Query & Quick Stats */}
            <div className="xl:col-span-1 space-y-6">
              <QueryPanel onQuery={handleQuery} loading={loading} />
              
              {/* Quick Stats Card */}
              {results && (
                <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6">
                  <div className="flex items-center space-x-2 mb-4">
                    <BarChart3 className="w-5 h-5 text-blue-400" />
                    <h3 className="text-lg font-semibold text-white">Quick Stats</h3>
                  </div>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400 text-sm">Data Rows</span>
                      <span className="text-white font-bold">{results.raw_rows?.length || 0}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400 text-sm">Source</span>
                      <span className="text-blue-400 text-sm font-medium">
                        {results.snowleopard_solution ? 'SnowLeopard' : 'Local'}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400 text-sm">Analysis</span>
                      <span className="text-white text-sm capitalize">
                        {results.analysis_type?.replace(/_/g, ' ')}
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Right Panel - Map and Results */}
            <div className="xl:col-span-2 space-y-6">
              {/* Map */}
              <MapView results={results} />
              
              {/* Charts */}
              {results && results.chart_data && (
                <ChartsPanel 
                  chartData={results.chart_data} 
                  onDownloadPDF={handleDownloadPDF}
                />
              )}
              
              {/* Results Panel */}
              {results && <ResultsPanel results={results} />}
            </div>
          </div>
        )}

        {activeView === 'map' && (
          <div className="space-y-6">
            {/* Query Bar */}
            <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-4">
              <QueryPanel onQuery={handleQuery} loading={loading} />
            </div>
            
            {/* Map */}
            <MapView results={results} />
            
            {/* Charts */}
            {results && results.chart_data && (
              <ChartsPanel 
                chartData={results.chart_data} 
                onDownloadPDF={handleDownloadPDF}
              />
            )}
            
            {/* Results */}
            {results && <ResultsPanel results={results} />}
          </div>
        )}

        {activeView === 'data' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Query Panel */}
            <div className="lg:col-span-1">
              <QueryPanel onQuery={handleQuery} loading={loading} />
            </div>
            
            {/* Full Results */}
            <div className="lg:col-span-2 space-y-6">
              {results ? (
                <>
                  {/* Charts */}
                  {results.chart_data && (
                    <ChartsPanel 
                      chartData={results.chart_data} 
                      onDownloadPDF={handleDownloadPDF}
                    />
                  )}
                  
                  {/* Results Panel */}
                  <ResultsPanel results={results} />
                </>
              ) : (
                <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-12 text-center">
                  <BarChart3 className="w-16 h-16 text-slate-600 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-white mb-2">No Data Yet</h3>
                  <p className="text-slate-400">Ask a question to see detailed analysis results</p>
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
