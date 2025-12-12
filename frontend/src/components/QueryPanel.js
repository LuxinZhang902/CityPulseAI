import React, { useState } from 'react';
import { Send, Zap, Mic, Camera, MapPin, AlertTriangle, Home } from 'lucide-react';

const EXAMPLE_QUERIES = [
  { 
    text: "Where is SF under the highest emergency stress right now?",
    icon: AlertTriangle,
    color: "text-red-400"
  },
  { 
    text: "Which neighborhoods show rising homelessness pressure this week?",
    icon: Home,
    color: "text-orange-400"
  },
  { 
    text: "Show a map of fire + hazmat incidents in the past 6 hours",
    icon: MapPin,
    color: "text-yellow-400"
  },
  { 
    text: "Explain why the Tenderloin is a hotspot",
    icon: Zap,
    color: "text-purple-400"
  }
];

function QueryPanel({ onQuery, loading }) {
  const [question, setQuestion] = useState('');
  const [isRecording, setIsRecording] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim() && !loading) {
      onQuery(question);
    }
  };

  const handleExampleClick = (example) => {
    setQuestion(example.text);
    onQuery(example.text);
  };

  const handleVoiceInput = () => {
    setIsRecording(!isRecording);
    // Voice input functionality would go here
  };

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6 shadow-xl">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="relative">
            <Zap className="w-6 h-6 text-blue-400" />
            <div className="absolute inset-0 w-6 h-6 bg-blue-400/20 rounded-full animate-ping"></div>
          </div>
          <h2 className="text-xl font-bold text-white">Ask CityPulse AI</h2>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          <span className="text-xs text-green-400">Live</span>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask about SF emergencies, disasters, homelessness, or infrastructure stress..."
            className="w-full px-4 py-3 bg-slate-900/50 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none transition-all"
            rows={4}
            disabled={loading}
          />
          <div className="absolute bottom-3 right-3 flex items-center space-x-2">
            <button
              type="button"
              onClick={handleVoiceInput}
              className={`p-2 rounded-lg transition-all ${
                isRecording 
                  ? 'bg-red-500 text-white animate-pulse' 
                  : 'bg-slate-700 text-slate-400 hover:bg-slate-600 hover:text-white'
              }`}
              disabled={loading}
            >
              <Mic className="w-4 h-4" />
            </button>
            <button
              type="button"
              className="p-2 bg-slate-700 text-slate-400 rounded-lg hover:bg-slate-600 hover:text-white transition-all"
              disabled={loading}
            >
              <Camera className="w-4 h-4" />
            </button>
          </div>
        </div>

        <button
          type="submit"
          disabled={!question.trim() || loading}
          className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 disabled:from-slate-700 disabled:to-slate-700 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg flex items-center justify-center space-x-2 transition-all transform hover:scale-[1.02] active:scale-[0.98] shadow-lg"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <Send className="w-5 h-5" />
              <span>Analyze</span>
            </>
          )}
        </button>
      </form>

      <div className="mt-6">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-semibold text-slate-400">Example Queries</h3>
          <span className="text-xs text-slate-500">Click to try</span>
        </div>
        <div className="space-y-2">
          {EXAMPLE_QUERIES.map((example, index) => {
            const Icon = example.icon;
            return (
              <button
                key={index}
                onClick={() => handleExampleClick(example)}
                disabled={loading}
                className="w-full text-left px-4 py-3 bg-slate-900/30 hover:bg-slate-900/50 border border-slate-700/50 rounded-lg text-sm text-slate-300 hover:text-white transition-all disabled:opacity-50 disabled:cursor-not-allowed group transform hover:scale-[1.02] active:scale-[0.98]"
              >
                <div className="flex items-center space-x-3">
                  <Icon className={`w-4 h-4 ${example.color} group-hover:scale-110 transition-transform`} />
                  <span className="flex-1">{example.text}</span>
                  <Send className="w-3 h-3 text-slate-500 group-hover:text-blue-400 transition-colors" />
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* AI Status */}
      <div className="mt-6 pt-4 border-t border-slate-700">
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></div>
            <span className="text-slate-400">Powered by SnowLeopard AI</span>
          </div>
          <span className="text-slate-500">Real-time analysis</span>
        </div>
      </div>
    </div>
  );
}

export default QueryPanel;
