import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axios';
import ProblemCard from '../components/ProblemCard';

const Daily = () => {
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/problems/today/')
       .then(res => {
         setAssignments(res.data);
         setLoading(false);
       })
       .catch(err => {
         console.error(err);
         setLoading(false);
       });
  }, []);

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="mb-8 pb-4 border-b border-slate-700 flex justify-between items-center">
        <h1 className="text-3xl font-bold text-emerald-400">Daily Driver</h1>
        <Link to="/dashboard" className="text-slate-400 hover:text-white">← Dashboard</Link>
      </div>

      {loading ? (
        <div className="text-slate-400 text-center py-20 font-bold animate-pulse">Loading today's problems & generating AI hints...</div>
      ) : assignments.length === 0 ? (
        <div className="bg-slate-800 p-6 text-center rounded text-slate-400">No problems assigned today. Make sure you are connected with a friend!</div>
      ) : (
        assignments.map((assignment) => (
          <ProblemCard 
            key={assignment.id} 
            assignmentId={assignment.id} 
            problem={assignment.problem} 
            isSolved={assignment.solved} 
          />
        ))
      )}
    </div>
  );
};
export default Daily;
