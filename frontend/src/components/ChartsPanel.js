import React from 'react';
import { BarChart3, PieChart, TrendingUp, Download } from 'lucide-react';

const ChartsPanel = ({ chartData, onDownloadPDF }) => {
  if (!chartData || !chartData.charts || chartData.charts.length === 0) {
    return (
      <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6 text-center">
        <BarChart3 className="w-12 h-12 text-slate-600 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-white mb-2">No Charts Available</h3>
        <p className="text-slate-400">Charts will be generated when data is available</p>
      </div>
    );
  }

  const renderChart = (chart) => {
    const { type, title, data, description } = chart;
    
    if (!data || !data.labels || !data.values || data.labels.length === 0) {
      return (
        <div className="bg-slate-900/50 border border-slate-700 rounded-lg p-8 text-center">
          <p className="text-slate-400">No data available for this chart</p>
        </div>
      );
    }

    // Simple CSS-based chart rendering
    const maxValue = Math.max(...data.values);
    const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16'];

    if (type === 'bar') {
      return (
        <div className="bg-slate-900/50 border border-slate-700 rounded-lg p-6">
          <div className="mb-4">
            <h4 className="text-lg font-semibold text-white">{title}</h4>
            <p className="text-sm text-slate-400">{description}</p>
          </div>
          <div className="space-y-3">
            {data.labels.map((label, index) => {
              const value = data.values[index];
              const percentage = (value / maxValue) * 100;
              const color = colors[index % colors.length];
              
              return (
                <div key={index} className="flex items-center space-x-3">
                  <div className="w-32 text-sm text-slate-300 truncate">{label}</div>
                  <div className="flex-1 bg-slate-800 rounded-full h-6 relative overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-500 ease-out"
                      style={{
                        width: `${percentage}%`,
                        backgroundColor: color
                      }}
                    />
                    <span className="absolute inset-0 flex items-center justify-center text-xs text-white font-medium">
                      {value}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      );
    }

    if (type === 'pie') {
      return (
        <div className="bg-slate-900/50 border border-slate-700 rounded-lg p-6">
          <div className="mb-4">
            <h4 className="text-lg font-semibold text-white">{title}</h4>
            <p className="text-sm text-slate-400">{description}</p>
          </div>
          <div className="grid grid-cols-2 gap-4">
            {data.labels.map((label, index) => {
              const value = data.values[index];
              const total = data.values.reduce((sum, val) => sum + val, 0);
              const percentage = ((value / total) * 100).toFixed(1);
              const color = colors[index % colors.length];
              
              return (
                <div key={index} className="flex items-center space-x-3">
                  <div
                    className="w-4 h-4 rounded-full"
                    style={{ backgroundColor: color }}
                  />
                  <div className="flex-1">
                    <div className="text-sm text-white font-medium">{label}</div>
                    <div className="text-xs text-slate-400">{value} ({percentage}%)</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      );
    }

    if (type === 'line') {
      return (
        <div className="bg-slate-900/50 border border-slate-700 rounded-lg p-6">
          <div className="mb-4">
            <h4 className="text-lg font-semibold text-white">{title}</h4>
            <p className="text-sm text-slate-400">{description}</p>
          </div>
          <div className="relative h-40">
            <svg className="w-full h-full" viewBox="0 0 400 160">
              {/* Grid lines */}
              {[0, 1, 2, 3, 4].map(i => (
                <line
                  key={i}
                  x1="40"
                  y1={32 * i + 16}
                  x2="380"
                  y2={32 * i + 16}
                  stroke="#475569"
                  strokeWidth="1"
                />
              ))}
              
              {/* Line chart */}
              <polyline
                points={data.values.map((value, index) => {
                  const x = 40 + (340 / (data.values.length - 1)) * index;
                  const y = 144 - (value / maxValue) * 112;
                  return `${x},${y}`;
                }).join(' ')}
                fill="none"
                stroke="#3b82f6"
                strokeWidth="2"
              />
              
              {/* Data points */}
              {data.values.map((value, index) => {
                const x = 40 + (340 / (data.values.length - 1)) * index;
                const y = 144 - (value / maxValue) * 112;
                return (
                  <circle
                    key={index}
                    cx={x}
                    cy={y}
                    r="4"
                    fill="#3b82f6"
                    stroke="#1e293b"
                    strokeWidth="2"
                  />
                );
              })}
              
              {/* X-axis labels */}
              {data.labels.map((label, index) => {
                const x = 40 + (340 / (data.labels.length - 1)) * index;
                return (
                  <text
                    key={index}
                    x={x}
                    y="156"
                    textAnchor="middle"
                    className="fill-slate-400 text-xs"
                  >
                    {label.split(':')[0]}
                  </text>
                );
              })}
            </svg>
          </div>
        </div>
      );
    }

    return (
      <div className="bg-slate-900/50 border border-slate-700 rounded-lg p-6">
        <h4 className="text-lg font-semibold text-white mb-2">{title}</h4>
        <p className="text-sm text-slate-400">Chart type '{type}' not yet supported</p>
      </div>
    );
  };

  const getChartIcon = (type) => {
    switch (type) {
      case 'bar': return <BarChart3 className="w-5 h-5" />;
      case 'pie': return <PieChart className="w-5 h-5" />;
      case 'line': return <TrendingUp className="w-5 h-5" />;
      default: return <BarChart3 className="w-5 h-5" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-blue-500/20 rounded-lg">
            <BarChart3 className="w-6 h-6 text-blue-400" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">Data Visualizations</h2>
            <p className="text-sm text-slate-400">Charts and insights powered by SnowLeopard AI</p>
          </div>
        </div>
        
        {onDownloadPDF && (
          <button
            onClick={onDownloadPDF}
            className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg hover:from-blue-700 hover:to-cyan-700 transition-all duration-200 shadow-lg"
          >
            <Download className="w-4 h-4" />
            <span>Download PDF Report</span>
          </button>
        )}
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {chartData.charts.map((chart, index) => (
          <div key={index} className="space-y-2">
            <div className="flex items-center space-x-2 text-sm text-slate-400">
              {getChartIcon(chart.type)}
              <span className="uppercase">{chart.type} Chart</span>
              {chart.suggested && (
                <span className="px-2 py-1 bg-purple-500/20 text-purple-400 text-xs rounded-full">
                  AI Suggested
                </span>
              )}
            </div>
            {renderChart(chart)}
          </div>
        ))}
      </div>

      {/* Chart Summary */}
      <div className="bg-gradient-to-r from-blue-500/10 to-cyan-500/10 border border-blue-500/30 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-3">Analysis Summary</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-400">{chartData.charts.length}</div>
            <div className="text-xs text-slate-400">Charts Generated</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-400">
              {chartData.charts.filter(c => c.type === 'bar').length}
            </div>
            <div className="text-xs text-slate-400">Bar Charts</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-400">
              {chartData.charts.filter(c => c.type === 'pie').length}
            </div>
            <div className="text-xs text-slate-400">Pie Charts</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-400">
              {chartData.charts.filter(c => c.type === 'line').length}
            </div>
            <div className="text-xs text-slate-400">Line Charts</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChartsPanel;
