import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axios';
import useAuthStore from '../store/auth';

const Dashboard = () => {
  const [friendReq, setFriendReq] = useState('');
  const [friend, setFriend] = useState(null);
  const [msg, setMsg] = useState('');
  const logout = useAuthStore(state => state.logout);

  useEffect(() => {
    api.get('/friends/my-friend/')
       .then(res => setFriend(res.data))
       .catch(() => {});
  }, []);

  const inviteFriend = async () => {
    try {
      await api.post('/friends/invite/', { username: friendReq });
      setMsg('Invite sent!');
    } catch {
      setMsg('Invite failed / User not found');
    }
  };

  const acceptFriend = async () => {
    try {
      await api.post('/friends/accept/', { username: friendReq });
      setMsg('Friend accepted! Week 1 starts now.');
      window.location.reload();
    } catch {
      setMsg('Accept failed');
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-8 pb-4 border-b border-slate-700">
        <h1 className="text-3xl font-bold text-emerald-400">Dashboard</h1>
        <button onClick={logout} className="text-slate-400 hover:text-white">Logout</button>
      </div>

      {!friend ? (
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 mb-8">
          <h2 className="text-xl font-bold mb-4">Connect with a Friend</h2>
          <div className="flex gap-2 mb-2">
            <input 
              placeholder="Friend's Username" 
              className="px-4 py-2 bg-slate-700 rounded border border-slate-600 flex-1"
              value={friendReq} onChange={e=>setFriendReq(e.target.value)}
            />
            <button onClick={inviteFriend} className="bg-emerald-500 text-slate-900 font-bold px-4 rounded">Invite</button>
            <button onClick={acceptFriend} className="bg-blue-500 text-white font-bold px-4 rounded">Accept</button>
          </div>
          <div className="text-sm text-slate-400">{msg}</div>
        </div>
      ) : (
        <div className="bg-emerald-500/20 text-emerald-400 p-4 rounded-xl border border-emerald-500/50 mb-8 font-bold flex items-center justify-between">
          <span>Connected with: {friend.username} ({friend.leetcode_username})</span>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
        <Link to="/daily" className="bg-slate-800 p-6 rounded-xl border border-slate-700 hover:border-emerald-500 transition-colors group">
          <h2 className="text-2xl font-bold text-slate-100 group-hover:text-emerald-400 mb-2">Today's Problems →</h2>
          <p className="text-slate-400 text-sm">Solve your 3 daily problems to earn points.</p>
        </Link>
        <Link to="/leaderboard" className="bg-slate-800 p-6 rounded-xl border border-slate-700 hover:border-blue-500 transition-colors group">
          <h2 className="text-2xl font-bold text-slate-100 group-hover:text-blue-400 mb-2">Leaderboard →</h2>
          <p className="text-slate-400 text-sm">Track your weekly points against your friend.</p>
        </Link>
      </div>
    </div>
  );
};
export default Dashboard;
