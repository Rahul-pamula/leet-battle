import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

const Locked = () => {
  const [week, setWeek] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    api.get('/competition/week/current/')
       .then(res => setWeek(res.data))
       .catch(console.error);
  }, []);

  const handlePay = async () => {
    if (!week) return;
    try {
      await api.post('/competition/unlock/', { week_id: week.id });
      navigate('/dashboard');
    } catch(err) {
      console.error(err);
    }
  };

  if (!week) return <div className="min-h-screen bg-slate-900 text-white flex items-center justify-center">Loading...</div>;

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-4">
      <div className="bg-slate-900 border border-red-500/50 p-10 rounded-2xl max-w-md w-full text-center shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-2 bg-red-500"></div>
        
        <div className="w-20 h-20 bg-slate-800 rounded-full flex items-center justify-center mx-auto mb-6 border border-slate-700">
          <span className="text-4xl">🔒</span>
        </div>

        <h1 className="text-3xl font-black text-white mb-2">Week is Locked</h1>
        {week.payment_status === 'tie' ? (
           <p className="text-slate-400 mb-8">It's a tie! Both of you can proceed freely.</p>
        ) : (
           <p className="text-slate-400 mb-8">You lost Week {week.id}. Pay the penalty to unlock Week {week.id + 1}.</p>
        )}

        {week.payment_status !== 'tie' && (
          <div className="bg-slate-950 p-6 rounded-xl border border-slate-800 mb-8">
            <div className="text-sm text-slate-500 mb-1">Amount Due</div>
            <div className="text-5xl font-black text-red-500 mb-4">₹{week.payment_amount}</div>
            <div className="text-xs text-slate-600 bg-slate-900 p-2 rounded">
              Formula: (Point Diff / 210) × 100
            </div>
          </div>
        )}

        <button 
          onClick={handlePay}
          className="w-full bg-red-600 hover:bg-red-500 text-white font-bold py-4 rounded-xl shadow-lg shadow-red-900/50 transition-all active:scale-95"
        >
          {week.payment_status === 'tie' ? 'Unlock Next Week' : 'Simulate Payment & Unlock'}
        </button>
      </div>
    </div>
  );
};
export default Locked;
