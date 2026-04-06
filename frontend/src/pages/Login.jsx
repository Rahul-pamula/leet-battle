import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api/axios';
import useAuthStore from '../store/auth';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const setToken = useAuthStore(state => state.setToken);
  const navigate = useNavigate();
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/auth/login/', { username, password });
      setToken(res.data.access);
      navigate('/dashboard');
    } catch {
      setError('Invalid credentials');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <form onSubmit={handleSubmit} className="bg-slate-800 p-8 rounded shadow-lg w-96">
        <h2 className="text-2xl font-bold mb-6 text-center text-emerald-400">DSA Battle Login</h2>
        {error && <div className="bg-red-500/20 text-red-500 p-2 rounded mb-4 text-center">{error}</div>}
        <input 
          className="w-full p-2 mb-4 bg-slate-700 border border-slate-600 rounded" 
          placeholder="Username" 
          value={username} onChange={e => setUsername(e.target.value)} 
        />
        <input 
          className="w-full p-2 mb-6 bg-slate-700 border border-slate-600 rounded" 
          type="password" 
          placeholder="Password" 
          value={password} onChange={e => setPassword(e.target.value)} 
        />
        <button type="submit" className="w-full bg-emerald-500 text-slate-900 font-bold py-2 rounded mb-4">
          Login
        </button>
        <p className="text-center text-sm text-slate-400">
          Don't have an account? <Link to="/signup" className="text-emerald-400">Sign Up</Link>
        </p>
      </form>
    </div>
  );
};
export default Login;
