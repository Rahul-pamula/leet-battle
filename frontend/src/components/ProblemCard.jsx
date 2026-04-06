import React, { useState } from 'react';
import api from '../api/axios';

const ProblemCard = ({ problem, assignmentId, isSolved, onSolved }) => {
  const [solved, setSolved] = useState(isSolved);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('python');
  const [error, setError] = useState('');
  const leetUrl = problem.leetcode_url || (problem.slug ? `https://leetcode.com/problems/${problem.slug}/` : '#');

  const handleSolve = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await api.post('/problems/mark-solved/', { assignment_id: assignmentId });
      setSolved(true);
      if (onSolved) onSolved();
      if (res.data?.points) {
        // optional: surface awarded points
      }
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.reason || 'Verification failed. Ensure you submitted an Accepted solution on LeetCode after the assignment time.');
    }
    setLoading(false);
  };

  const getDifficultyColor = (diff) => {
    if (diff === 'easy') return 'bg-green-600 text-white';
    if (diff === 'medium') return 'bg-yellow-500 text-white';
    return 'bg-red-600 text-white';
  };

  return (
    <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-xl mb-6">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-3">
            <span className="text-xs bg-purple-700/60 text-purple-100 px-2 py-1 rounded-full">Q{problem.order_in_step}</span>
            {problem.title}
            <span className={`text-xs px-2 py-1 uppercase tracking-widest font-bold rounded ${getDifficultyColor(problem.difficulty)}`}>
              {problem.difficulty}
            </span>
          </h2>
          <div className="flex gap-2 mt-2">
            <span className="text-xs bg-slate-700 text-slate-300 px-2 py-1 rounded-full">
              {problem.topic_tag}
            </span>
            <a
              href={leetUrl}
              target="_blank"
              rel="noreferrer"
              className="text-xs bg-blue-600 hover:bg-blue-500 text-white px-2 py-1 rounded-full transition-colors"
            >
              LeetCode →
            </a>
            <a
              href="https://takeuforward.org/dsa/strivers-a2z-sheet-learn-dsa-a-to-z"
              target="_blank"
              rel="noreferrer"
              className="text-xs bg-emerald-700 hover:bg-emerald-600 text-white px-2 py-1 rounded-full transition-colors"
            >
              Striver A2Z ↗
            </a>
          </div>
        </div>
        <div>
          <button 
            disabled={solved || loading}
            onClick={handleSolve}
            className={`px-4 py-2 font-bold rounded transition-colors ${solved ? 'bg-green-600 text-white opacity-50 cursor-not-allowed' : 'bg-emerald-500 hover:bg-emerald-400 text-slate-900'}`}
          >
            {solved ? '✓ Verified' : loading ? 'Verifying…' : 'Verify on LeetCode'}
          </button>
        </div>
      </div>
      {error && <div className="text-sm text-red-400 mb-3">{error}</div>}

      <div className="mt-6 border-t border-slate-700 pt-4">
        <h3 className="text-md font-semibold text-emerald-400 mb-2">Pattern: {problem.pattern_name || 'Loading AI Pattern...'}</h3>
        <p className="text-sm text-slate-300 mb-4">{problem.pattern_explanation}</p>

        <div className="flex gap-4 mb-4 text-xs text-slate-400">
          <div><span className="font-bold text-slate-300">Time:</span> {problem.time_complexity}</div>
          <div><span className="font-bold text-slate-300">Space:</span> {problem.space_complexity}</div>
        </div>

        <div className="bg-slate-900 rounded-lg overflow-hidden border border-slate-700">
          <div className="flex bg-slate-800 border-b border-slate-700">
            <button 
              className={`flex-1 py-3 text-sm font-bold uppercase transition-colors ${activeTab === 'python' ? 'bg-slate-700 text-emerald-400 border-b-2 border-emerald-400' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700'}`}
              onClick={() => setActiveTab('python')}
            >
              Python
            </button>
            <button 
              className={`flex-1 py-3 text-sm font-bold uppercase transition-colors ${activeTab === 'java' ? 'bg-slate-700 text-emerald-400 border-b-2 border-emerald-400' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-700'}`}
              onClick={() => setActiveTab('java')}
            >
              Java
            </button>
          </div>
          <pre className="p-4 overflow-x-auto text-xs text-slate-300">
            <code>
              {activeTab === 'python' ? problem.python_template : problem.java_template}
            </code>
          </pre>
        </div>
      </div>
    </div>
  );
};

export default ProblemCard;
