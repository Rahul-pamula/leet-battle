import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api/axios';
import useAuthStore from '../store/auth';

const Signup = () => {
  const [form, setForm] = useState({ username: '', email: '', password: '', leetcode_username: '', language: 'python' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post('/auth/signup/', form);
      // Auto login after signup
      const res = await api.post('/auth/login/', { username: form.username, password: form.password });
      useAuthStore.getState().setToken(res.data.access);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.leetcode_username?.[0] || 'Signup failed');
    }
    setLoading(false);
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <form onSubmit={handleSubmit} className="bg-slate-800 p-8 rounded shadow-lg w-96">
        <h2 className="text-2xl font-bold mb-6 text-center text-emerald-400">DSA Battle Signup</h2>
        {error && <div className="bg-red-500/20 text-red-500 p-2 rounded mb-4 text-center">{error}</div>}
        <input className="w-full p-2 mb-3 bg-slate-700 border border-slate-600 rounded" placeholder="Username" value={form.username} onChange={e => setForm({...form, username: e.target.value})} required/>
        <input className="w-full p-2 mb-3 bg-slate-700 border border-slate-600 rounded" type="email" placeholder="Email" value={form.email} onChange={e => setForm({...form, email: e.target.value})} required/>
        <input className="w-full p-2 mb-3 bg-slate-700 border border-slate-600 rounded" type="password" placeholder="Password" value={form.password} onChange={e => setForm({...form, password: e.target.value})} required/>
        <input className="w-full p-2 mb-3 bg-slate-700 border border-slate-600 rounded border-l-4 border-l-blue-500" placeholder="LeetCode Username (validated)" value={form.leetcode_username} onChange={e => setForm({...form, leetcode_username: e.target.value})} required/>
        <select className="w-full p-2 mb-6 bg-slate-700 border border-slate-600 rounded" value={form.language} onChange={e => setForm({...form, language: e.target.value})}>
          <option value="python">Python</option>
          <option value="java">Java</option>
        </select>
        <button disabled={loading} type="submit" className="w-full bg-emerald-500 text-slate-900 font-bold py-2 rounded mb-4 disabled:opacity-50">
          {loading ? 'Validating LeetCode...' : 'Sign Up'}
        </button>
        <p className="text-center text-sm text-slate-400">
           Have an account? <Link to="/login" className="text-emerald-400">Login</Link>
        </p>
      </form>
    </div>
  );
};
export default Signup;
