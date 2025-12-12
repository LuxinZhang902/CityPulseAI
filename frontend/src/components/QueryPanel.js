import React, { useState } from 'react';
import { Send, Zap } from 'lucide-react';

const EXAMPLE_QUERIES = [
  "Where is SF under the highest emergency stress right now?",
  "Which neighborhoods show rising homelessness pressure this week?",
  "Show a map of fire + hazmat incidents in the past 6 hours",
  "Explain why the Tenderloin is a hotspot"
];

function QueryPanel({ onQuery, loading }) {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim() && !loading) {
      onQuery(question);
    }
  };

  const handleExampleClick = (example) => {
    setQuestion(example);
    onQuery(example);
  };

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 rounded-lg p-6">
      <div className="flex items-center space-x-2 mb-4">
        <Zap className="w-5 h-5 text-blue-400" />
        <h2 className="text-xl font-bold text-white">Ask CityPulse AI</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask about SF emergencies, disasters, homelessness, or infrastructure stress..."
            className="w-full px-4 py-3 bg-slate-900/50 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            rows={4}
            disabled={loading}
          />
        </div>

        <button
          type="submit"
          disabled={!question.trim() || loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white font-semibold py-3 px-4 rounded-lg flex items-center justify-center space-x-2 transition-colors"
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
        <h3 className="text-sm font-semibold text-slate-400 mb-3">Example Queries</h3>
        <div className="space-y-2">
          {EXAMPLE_QUERIES.map((example, index) => (
            <button
              key={index}
              onClick={() => handleExampleClick(example)}
              disabled={loading}
              className="w-full text-left px-3 py-2 bg-slate-900/30 hover:bg-slate-900/50 border border-slate-700/50 rounded text-sm text-slate-300 hover:text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default QueryPanel;
