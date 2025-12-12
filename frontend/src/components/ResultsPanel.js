import React, { useState } from 'react';
import { TrendingUp, AlertTriangle, Code, ChevronDown, ChevronUp } from 'lucide-react';

function ResultsPanel({ results }) {
  const [showSQL, setShowSQL] = useState(false);
  const [showRawData, setShowRawData] = useState(false);

  if (!results) {
    return null;
  }

  const getSeverityColor = (severity) => {
    const severityMap = {
      critical: 'text-red-400 bg-red-500/10 border-red-500/50',
      high: 'text-orange-400 bg-orange-500/10 border-orange-500/50',
      medium: 'text-yellow-400 bg-yellow-500/10 border-yellow-500/50',
      low: 'text-green-400 bg-green-500/10 border-green-500/50',
    };
    return severityMap[severity] || severityMap.medium;
  };

  return (
    <div className="space-y-4">
      <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6">
        <div className="flex items-center space-x-2 mb-4">
          <TrendingUp className="w-5 h-5 text-blue-400" />
          <h2 className="text-xl font-bold text-white">Analysis Results</h2>
        </div>

        <div className="mb-4">
          <div className="text-sm text-slate-400 mb-1">Analysis Type</div>
          <div className="text-white font-semibold capitalize">
            {results.analysis_type?.replace(/_/g, ' ')}
          </div>
        </div>

        <div className="mb-4">
          <div className="text-sm text-slate-400 mb-2">Key Insights</div>
          <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
            <p className="text-blue-100 text-sm leading-relaxed">
              {results.insight_summary}
            </p>
          </div>
        </div>

        {results.top_neighborhoods && results.top_neighborhoods.length > 0 && (
          <div>
            <div className="text-sm text-slate-400 mb-2">Top Affected Neighborhoods</div>
            <div className="space-y-2">
              {results.top_neighborhoods.slice(0, 5).map((neighborhood, index) => (
                <div
                  key={index}
                  className="bg-slate-900/50 border border-slate-700 rounded-lg p-3"
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center text-white text-xs font-bold">
                        {index + 1}
                      </div>
                      <span className="text-white font-semibold">{neighborhood.name}</span>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    {Object.entries(neighborhood.metrics || {}).map(([key, value]) => (
                      <div key={key} className="flex justify-between">
                        <span className="text-slate-400">{key.replace(/_/g, ' ')}:</span>
                        <span className="text-white font-mono">
                          {typeof value === 'number' ? value.toFixed(2) : value}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6">
        <button
          onClick={() => setShowSQL(!showSQL)}
          className="w-full flex items-center justify-between text-left"
        >
          <div className="flex items-center space-x-2">
            <Code className="w-5 h-5 text-blue-400" />
            <h3 className="text-lg font-semibold text-white">SQL Query Used</h3>
          </div>
          {showSQL ? (
            <ChevronUp className="w-5 h-5 text-slate-400" />
          ) : (
            <ChevronDown className="w-5 h-5 text-slate-400" />
          )}
        </button>

        {showSQL && (
          <div className="mt-4">
            <pre className="bg-slate-900 border border-slate-700 rounded-lg p-4 overflow-x-auto text-xs text-green-400 font-mono">
              {results.sql_used}
            </pre>
          </div>
        )}
      </div>

      {results.raw_rows && results.raw_rows.length > 0 && (
        <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6">
          <button
            onClick={() => setShowRawData(!showRawData)}
            className="w-full flex items-center justify-between text-left"
          >
            <div className="flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5 text-blue-400" />
              <h3 className="text-lg font-semibold text-white">
                Raw Data ({results.raw_rows.length} rows)
              </h3>
            </div>
            {showRawData ? (
              <ChevronUp className="w-5 h-5 text-slate-400" />
            ) : (
              <ChevronDown className="w-5 h-5 text-slate-400" />
            )}
          </button>

          {showRawData && (
            <div className="mt-4 overflow-x-auto">
              <table className="w-full text-xs">
                <thead>
                  <tr className="border-b border-slate-700">
                    {Object.keys(results.raw_rows[0]).map((key) => (
                      <th key={key} className="text-left py-2 px-3 text-slate-400 font-semibold">
                        {key}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {results.raw_rows.map((row, index) => (
                    <tr key={index} className="border-b border-slate-800">
                      {Object.values(row).map((value, i) => (
                        <td key={i} className="py-2 px-3 text-slate-300 font-mono">
                          {typeof value === 'number' ? value.toFixed(2) : value || '-'}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default ResultsPanel;
