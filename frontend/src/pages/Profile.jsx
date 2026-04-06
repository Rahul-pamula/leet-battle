import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axios';

const Profile = () => {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    api.get('/competition/profile/')
       .then(res => setProfile(res.data))
       .catch(console.error);
  }, []);

  if (!profile) return <div className="p-8 text-center animate-pulse">Loading Profile...</div>;

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="mb-8 pb-4 border-b border-slate-700 flex justify-between items-center">
        <h1 className="text-3xl font-bold text-emerald-400">Profile</h1>
        <Link to="/dashboard" className="text-slate-400 hover:text-white">← Dashboard</Link>
      </div>

      <div className="flex items-center gap-6 mb-10 bg-slate-800 p-8 rounded-2xl border border-slate-700 shadow-xl">
        <div className="w-24 h-24 bg-gradient-to-tr from-emerald-400 to-blue-500 rounded-full flex items-center justify-center text-3xl font-black text-slate-900 shadow-inner">
          {profile.username[0].toUpperCase()}
        </div>
        <div>
          <h2 className="text-3xl font-bold text-white mb-2">{profile.username}</h2>
          <div className="flex gap-3 text-sm">
            <span className="bg-slate-700 px-3 py-1 rounded-full text-slate-300">LeetCode: {profile.leetcode_username}</span>
            <span className="bg-slate-700 px-3 py-1 rounded-full text-slate-300 uppercase">{profile.language}</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 text-center">
          <div className="text-xs text-slate-400 uppercase tracking-widest font-bold mb-2">Solved This Week</div>
          <div className="text-3xl font-black text-white">{profile.problems_solved_this_week}<span className="text-sm text-slate-500 font-normal">/21</span></div>
        </div>
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 text-center">
          <div className="text-xs text-slate-400 uppercase tracking-widest font-bold mb-2">Points This Week</div>
          <div className="text-3xl font-black text-emerald-400">{profile.points_this_week}</div>
        </div>
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 text-center opacity-50">
          <div className="text-xs text-slate-400 uppercase tracking-widest font-bold mb-2">Current Streak</div>
          <div className="text-3xl font-black text-white">0</div>
        </div>
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 text-center opacity-50">
          <div className="text-xs text-slate-400 uppercase tracking-widest font-bold mb-2">Weeks Won</div>
          <div className="text-3xl font-black text-white">{profile.wins}</div>
        </div>
      </div>
    </div>
  );
};
export default Profile;
