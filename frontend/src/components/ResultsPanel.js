import React, { useState } from 'react';
import { 
  MapPin, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle, 
  ChevronDown, 
  ChevronUp,
  Code,
  Brain,
  BarChart3,
  FileText,
  Target,
  Lightbulb,
  Shield,
  Download,
  Database,
  Clock
} from 'lucide-react';

function ResultsPanel({ results }) {
  const [showSQL, setShowSQL] = useState(false);
  const [showRawData, setShowRawData] = useState(false);
  const [showTechnical, setShowTechnical] = useState(false);
  const [showCharts, setShowCharts] = useState(true);
  const [downloadingPDF, setDownloadingPDF] = useState(false);

  if (!results) {
    return null;
  }

  const handleDownloadPDF = async () => {
    setDownloadingPDF(true);
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
        a.href = url;
        a.download = `citypulse-report-${Date.now()}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        alert('Failed to generate PDF report');
      }
    } catch (error) {
      console.error('Error downloading PDF:', error);
      alert('Error downloading PDF report');
    } finally {
      setDownloadingPDF(false);
    }
  };

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
      {/* Enhanced Analysis Summary Card */}
      <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6 shadow-xl">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <Brain className="w-7 h-7 text-purple-400" />
              <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-purple-400 rounded-full animate-pulse"></div>
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">SnowLeopard AI Analysis</h3>
              <p className="text-sm text-slate-400">Comprehensive intelligence report</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            {results.snowleopard_solution && (
              <div className="px-3 py-1 bg-gradient-to-r from-purple-500/20 to-pink-500/20 border border-purple-500/30 rounded-full">
                <span className="text-xs text-purple-300 font-medium">AI Powered</span>
              </div>
            )}
            <button
              onClick={handleDownloadPDF}
              disabled={downloadingPDF}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 disabled:bg-blue-500/50 text-white rounded-lg transition-all shadow-lg hover:shadow-blue-500/50"
            >
              <Download className="w-4 h-4" />
              <span className="text-sm font-medium">
                {downloadingPDF ? 'Generating...' : 'Download PDF'}
              </span>
            </button>
          </div>
        </div>

        {/* Executive Summary */}
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-white mb-3 flex items-center">
            <FileText className="w-5 h-5 mr-2 text-blue-400" />
            Executive Summary
          </h4>
          <p className="text-slate-300 leading-relaxed">
            {results.comprehensive_analysis?.executive_summary || results.insight_summary}
          </p>
        </div>

        {/* Key Insights Grid */}
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-white mb-3 flex items-center">
            <Lightbulb className="w-5 h-5 mr-2 text-yellow-400" />
            Key Insights
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {(results.comprehensive_analysis?.key_insights || results.key_insights || []).map((insight, index) => (
              <div key={index} className="flex items-start space-x-2 p-3 bg-slate-700/30 rounded-lg border border-slate-600/30">
                <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 flex-shrink-0"></div>
                <p className="text-sm text-slate-300 leading-relaxed">{insight}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Risk Assessment */}
        {results.comprehensive_analysis?.risk_assessment && (
          <div className="mb-6">
            <h4 className="text-lg font-semibold text-white mb-3 flex items-center">
              <Shield className="w-5 h-5 mr-2 text-red-400" />
              Risk Assessment
            </h4>
            <div className="flex items-center space-x-4 p-4 bg-slate-700/30 rounded-lg border border-slate-600/30">
              <div className="flex items-center space-x-2">
                <div className={`w-3 h-3 rounded-full ${
                  results.comprehensive_analysis.risk_assessment.level === 'LOW' ? 'bg-green-400' :
                  results.comprehensive_analysis.risk_assessment.level === 'MEDIUM' ? 'bg-yellow-400' :
                  results.comprehensive_analysis.risk_assessment.level === 'HIGH' ? 'bg-orange-400' :
                  'bg-red-400'
                }`}></div>
                <span className="text-lg font-bold text-white">
                  {results.comprehensive_analysis.risk_assessment.level}
                </span>
              </div>
              <div className="flex-1">
                <p className="text-sm text-slate-300">
                  {results.comprehensive_analysis.risk_assessment.reasoning}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Recommendations */}
        {results.comprehensive_analysis?.recommendations && (
          <div className="mb-6">
            <h4 className="text-lg font-semibold text-white mb-3 flex items-center">
              <Target className="w-5 h-5 mr-2 text-green-400" />
              Recommendations
            </h4>
            <div className="space-y-2">
              {results.comprehensive_analysis.recommendations.map((rec, index) => (
                <div key={index} className="flex items-start space-x-3 p-3 bg-gradient-to-r from-green-500/10 to-emerald-500/10 rounded-lg border border-green-500/30">
                  <div className="w-6 h-6 bg-green-500/20 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-xs text-green-400 font-bold">{index + 1}</span>
                  </div>
                  <p className="text-sm text-slate-300 leading-relaxed">{rec}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Top Neighborhoods */}
        {results.top_neighborhoods && results.top_neighborhoods.length > 0 && (
          <div className="mb-6">
            <h4 className="text-lg font-semibold text-white mb-3 flex items-center">
              <MapPin className="w-5 h-5 mr-2 text-blue-400" />
              Top Affected Areas
            </h4>
            <div className="space-y-2">
              {results.top_neighborhoods.slice(0, 5).map((neighborhood, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg border border-slate-600/30">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-blue-500/20 rounded-full flex items-center justify-center">
                      <span className="text-xs text-blue-400 font-bold">{index + 1}</span>
                    </div>
                    <span className="text-white font-medium">{neighborhood.name}</span>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold text-blue-400">{neighborhood.count}</div>
                    <div className="text-xs text-slate-400">incidents</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Analysis Metadata */}
        <div className="grid grid-cols-3 gap-4 pt-4 border-t border-slate-700">
          <div className="text-center">
            <div className="text-2xl font-bold text-white">{results.raw_rows?.length || 0}</div>
            <div className="text-xs text-slate-400">Records Analyzed</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-400">
              {results.comprehensive_analysis ? 'AI' : 'Local'}
            </div>
            <div className="text-xs text-slate-400">Analysis Method</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-400">
              {results.confidence ? `${Math.round(results.confidence * 100)}%` : 'N/A'}
            </div>
            <div className="text-xs text-slate-400">Confidence Score</div>
          </div>
        </div>
      </div>

        {/* Top Affected Neighborhoods */}
        {results.top_neighborhoods && results.top_neighborhoods.length > 0 && (
          <div>
            <div className="text-sm text-slate-400 mb-3">Top Affected Neighborhoods</div>
            <div className="space-y-2">
              {results.top_neighborhoods.slice(0, 3).map((neighborhood, index) => (
                <div
                  key={index}
                  className="bg-slate-900/50 border border-slate-700 rounded-lg p-3 hover:bg-slate-900/70 transition-all"
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-3">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-bold ${
                        index === 0 ? 'bg-red-500' : index === 1 ? 'bg-orange-500' : 'bg-yellow-500'
                      }`}>
                        {index + 1}
                      </div>
                      <span className="text-white font-semibold">{neighborhood.name}</span>
                    </div>
                    <BarChart3 className="w-4 h-4 text-slate-400" />
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    {Object.entries(neighborhood.metrics || {}).slice(0, 4).map(([key, value]) => (
                      <div key={key} className="flex justify-between">
                        <span className="text-slate-400">{key.replace(/_/g, ' ')}:</span>
                        <span className="text-white font-mono">
                          {typeof value === 'number' ? value.toFixed(0) : value}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

      {/* Charts Visualization Section */}
      {results.chart_data && results.chart_data.charts && results.chart_data.charts.length > 0 && (
        <div className="bg-slate-800/50 backdrop-blur-sm border border-purple-500/20 rounded-lg shadow-xl overflow-hidden">
          <div className="p-6 border-b border-purple-500/20">
            <button
              onClick={() => setShowCharts(!showCharts)}
              className="w-full flex items-center justify-between text-left"
            >
              <div className="flex items-center space-x-3">
                <div className="relative">
                  <BarChart3 className="w-6 h-6 text-purple-400" />
                  <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-purple-400 rounded-full animate-pulse"></div>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white">Data Visualizations</h3>
                  <p className="text-sm text-slate-400">
                    {results.chart_data.charts.length} chart{results.chart_data.charts.length > 1 ? 's' : ''} generated from analysis
                  </p>
                </div>
              </div>
              {showCharts ? (
                <ChevronUp className="w-5 h-5 text-slate-400" />
              ) : (
                <ChevronDown className="w-5 h-5 text-slate-400" />
              )}
            </button>

            {showCharts && (
              <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                {results.chart_data.charts.map((chart, index) => (
                  <div key={index} className="bg-slate-900/50 border border-slate-700 rounded-lg p-4">
                    <div className="mb-4">
                      <h4 className="text-md font-semibold text-white mb-1">{chart.title}</h4>
                      <p className="text-xs text-slate-400">{chart.description}</p>
                    </div>
                    
                    {/* Simple Bar Chart Visualization */}
                    {chart.type === 'bar' && chart.data && chart.data.labels && (
                      <div className="space-y-2">
                        {chart.data.labels.map((label, i) => {
                          const value = chart.data.values[i];
                          const maxValue = Math.max(...chart.data.values);
                          const percentage = (value / maxValue) * 100;
                          return (
                            <div key={i} className="space-y-1">
                              <div className="flex justify-between text-xs">
                                <span className="text-slate-300 truncate max-w-[60%]">{label}</span>
                                <span className="text-white font-mono">{value}</span>
                              </div>
                              <div className="w-full bg-slate-700 rounded-full h-2">
                                <div
                                  className={`h-2 rounded-full ${chart.color === 'danger' ? 'bg-red-500' : 'bg-blue-500'}`}
                                  style={{ width: `${percentage}%` }}
                                ></div>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    )}

                    {/* Simple Pie Chart Visualization */}
                    {chart.type === 'pie' && chart.data && chart.data.labels && (
                      <div className="space-y-2">
                        {chart.data.labels.map((label, i) => {
                          const value = chart.data.values[i];
                          const total = chart.data.values.reduce((a, b) => a + b, 0);
                          const percentage = ((value / total) * 100).toFixed(1);
                          const colors = ['bg-blue-500', 'bg-purple-500', 'bg-pink-500', 'bg-orange-500', 'bg-green-500', 'bg-yellow-500', 'bg-red-500', 'bg-indigo-500'];
                          return (
                            <div key={i} className="flex items-center justify-between text-xs">
                              <div className="flex items-center space-x-2 flex-1 truncate">
                                <div className={`w-3 h-3 rounded-full ${colors[i % colors.length]}`}></div>
                                <span className="text-slate-300 truncate">{label}</span>
                              </div>
                              <div className="flex items-center space-x-2">
                                <span className="text-white font-mono">{value}</span>
                                <span className="text-slate-400">({percentage}%)</span>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    )}

                    {/* Grouped Bar Chart */}
                    {chart.type === 'grouped_bar' && chart.data && chart.data.datasets && (
                      <div className="space-y-3">
                        {chart.data.labels.map((label, i) => (
                          <div key={i} className="space-y-1">
                            <div className="text-xs text-slate-300 font-medium">{label}</div>
                            {chart.data.datasets.map((dataset, j) => {
                              const value = dataset.values[i];
                              const maxValue = Math.max(...dataset.values);
                              const percentage = (value / maxValue) * 100;
                              return (
                                <div key={j} className="flex items-center space-x-2">
                                  <span className="text-xs text-slate-400 w-20 truncate">{dataset.label}</span>
                                  <div className="flex-1 bg-slate-700 rounded-full h-2">
                                    <div
                                      className="h-2 rounded-full"
                                      style={{ width: `${percentage}%`, backgroundColor: dataset.color }}
                                    ></div>
                                  </div>
                                  <span className="text-xs text-white font-mono w-12 text-right">{value}</span>
                                </div>
                              );
                            })}
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Line Chart (simplified as list) */}
                    {chart.type === 'line' && chart.data && chart.data.labels && (
                      <div className="space-y-1 max-h-48 overflow-y-auto">
                        {chart.data.labels.map((label, i) => {
                          const value = chart.data.values[i];
                          return (
                            <div key={i} className="flex justify-between text-xs py-1 border-b border-slate-700/50">
                              <span className="text-slate-300">{label}</span>
                              <span className="text-white font-mono">{value}</span>
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* SQL Query Card - Enhanced */}
      <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg shadow-xl overflow-hidden">
        <div className="p-6 border-b border-blue-500/20">
          <button
            onClick={() => setShowSQL(!showSQL)}
            className="w-full flex items-center justify-between text-left"
          >
            <div className="flex items-center space-x-3">
              <div className="relative">
                <Code className="w-6 h-6 text-green-400" />
                <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-white">SQL Query Analysis</h3>
                <p className="text-sm text-slate-400">
                  Generated via {results.sql_source || 'SnowLeopard AI'}
                </p>
              </div>
            </div>
            {showSQL ? (
              <ChevronUp className="w-5 h-5 text-slate-400" />
            ) : (
              <ChevronDown className="w-5 h-5 text-slate-400" />
            )}
          </button>

          {showSQL && (
            <div className="mt-4 space-y-4">
              <div className="bg-slate-900 border border-slate-700 rounded-lg p-4">
                <h4 className="text-sm font-semibold text-slate-300 mb-2">Generated SQL</h4>
                <pre className="text-xs text-green-400 font-mono overflow-x-auto whitespace-pre-wrap">
                  {results.sql_used}
                </pre>
              </div>
              
              {results.sql_explanation && (
                <div className="bg-slate-900 border border-slate-700 rounded-lg p-4">
                  <h4 className="text-sm font-semibold text-slate-300 mb-2">Explanation</h4>
                  <p className="text-xs text-slate-400">{results.sql_explanation}</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Raw Data Card - Enhanced */}
      {results.raw_rows && results.raw_rows.length > 0 && (
        <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg shadow-xl overflow-hidden">
          <div className="p-6 border-b border-blue-500/20">
            <button
              onClick={() => setShowRawData(!showRawData)}
              className="w-full flex items-center justify-between text-left"
            >
              <div className="flex items-center space-x-3">
                <Database className="w-6 h-6 text-blue-400" />
                <div>
                  <h3 className="text-lg font-semibold text-white">Raw Data ({results.raw_rows.length} rows)</h3>
                  <p className="text-sm text-slate-400">
                    Complete dataset from query execution
                  </p>
                </div>
              </div>
              {showRawData ? (
                <ChevronUp className="w-5 h-5 text-slate-400" />
              ) : (
                <ChevronDown className="w-5 h-5 text-slate-400" />
              )}
            </button>

            {showRawData && (
              <div className="mt-4 overflow-x-auto">
                <div className="bg-slate-900 border border-slate-700 rounded-lg overflow-hidden">
                  <table className="w-full text-xs">
                    <thead>
                      <tr className="border-b border-slate-700 bg-slate-800/50">
                        {Object.keys(results.raw_rows[0]).map((key) => (
                          <th key={key} className="text-left py-3 px-4 text-slate-300 font-semibold">
                            {key.replace(/_/g, ' ').toUpperCase()}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {results.raw_rows.slice(0, 10).map((row, index) => (
                        <tr key={index} className="border-b border-slate-800 hover:bg-slate-800/30 transition-colors">
                          {Object.values(row).map((value, i) => (
                            <td key={i} className="py-3 px-4 text-slate-300 font-mono">
                              {typeof value === 'number' ? value.toLocaleString() : value || '-'}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {results.raw_rows.length > 10 && (
                    <div className="p-3 text-center text-xs text-slate-500 border-t border-slate-700">
                      Showing 10 of {results.raw_rows.length} rows
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default ResultsPanel;
