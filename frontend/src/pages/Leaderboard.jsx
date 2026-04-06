import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api/axios';

const Leaderboard = () => {
  const [data, setData] = useState(null);
  const [week, setWeek] = useState(null);
  const navigate = useNavigate();
  const [oppList, setOppList] = useState([]);

  useEffect(() => {
    api.get('/competition/leaderboard/')
       .then(res => setData(res.data))
       .catch(console.error);

    api.get('/competition/week/current/')
       .then(res => {
         setWeek(res.data);
         setOppList(res.data.opponent_assignments || []);
       })
       .catch(console.error);
  }, []);

  const endWeek = async () => {
    if (!week) return;
    try {
      const res = await api.post('/competition/week/end/', { week_id: week.id });
      if (res.data.payment_status === 'pending' || res.data.payment_status === 'tie') {
        navigate('/locked');
      }
    } catch (err) {
      console.error(err);
    }
  };

  if (!data) return <div className="p-8 text-center animate-pulse">Loading Leaderboard...</div>;

  const totalPoints = Math.max(data.user_a.points + data.user_b.points, 1);
  const aPercent = (data.user_a.points / totalPoints) * 100;
  const bPercent = (data.user_b.points / totalPoints) * 100;

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="mb-8 pb-4 border-b border-slate-700 flex justify-between items-center">
        <h1 className="text-3xl font-bold text-emerald-400">Weekly Leaderboard</h1>
        <Link to="/dashboard" className="text-slate-400 hover:text-white">← Dashboard</Link>
      </div>

      <div className="grid grid-cols-2 gap-8 mb-8">
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 text-center shadow-lg">
          <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">{data.user_a.username[0].toUpperCase()}</div>
          <h2 className="text-2xl font-bold">{data.user_a.username}</h2>
          <div className="text-4xl font-black text-blue-400 mt-4">{data.user_a.points} <span className="text-lg text-slate-500">pts</span></div>
        </div>

        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 text-center shadow-lg">
          <div className="w-16 h-16 bg-red-600 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">{data.user_b.username[0].toUpperCase()}</div>
          <h2 className="text-2xl font-bold">{data.user_b.username}</h2>
          <div className="text-4xl font-black text-red-400 mt-4">{data.user_b.points} <span className="text-lg text-slate-500">pts</span></div>
        </div>
      </div>

      <div className="h-6 w-full rounded-full overflow-hidden flex bg-slate-800 border border-slate-700 mb-8 shadow-xl">
        <div style={{ width: `${aPercent}%` }} className="bg-blue-500 h-full transition-all duration-1000"></div>
        <div style={{ width: `${bPercent}%` }} className="bg-red-500 h-full transition-all duration-1000"></div>
      </div>

      <div className="text-center mt-12">
        <p className="text-slate-400 mb-4">Ends on {data.end_date}</p>
        <button onClick={endWeek} className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 px-8 rounded-full shadow-lg transition-colors">
          Simulate End of Week
        </button>
      </div>

      {oppList.length > 0 && (
        <div className="mt-10 bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg">
          <h3 className="text-xl font-bold text-slate-100 mb-4">Your friend's assignments</h3>
          <div className="space-y-3">
            {oppList.map(item => {
              const url = item.problem?.leetcode_url || (item.problem?.slug ? `https://leetcode.com/problems/${item.problem.slug}/` : '#');
              return (
                <div key={`${item.assigned_date}-${url}`} className="flex justify-between items-center bg-slate-900 px-3 py-2 rounded border border-slate-700">
                  <div>
                    <div className="text-slate-200 font-semibold">{item.problem?.title || 'Problem'}</div>
                    <div className="text-xs text-slate-500">Assigned: {item.assigned_date}</div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className={`text-xs px-2 py-1 rounded-full ${item.solved ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300'}`}>
                      {item.solved ? 'Solved' : 'Pending'}
                    </span>
                    <a className="text-xs text-blue-400 hover:text-blue-200" href={url} target="_blank" rel="noreferrer">View</a>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
export default Leaderboard;
