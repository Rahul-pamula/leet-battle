import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import useAuthStore from './store/auth';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import Daily from './pages/Daily';
import Leaderboard from './pages/Leaderboard';
import Profile from './pages/Profile';
import Locked from './pages/Locked';
import api from './api/axios';

const PrivateRoute = ({ children }) => {
  const token = useAuthStore(state => state.token);
  const location = useLocation();
  const [checked, setChecked] = useState(false);
  const [locked, setLocked] = useState(false);

  useEffect(() => {
    if (!token) return;
    api.get('/auth/me/')
       .then(res => setLocked(res.data.is_locked))
       .catch(() => setLocked(false))
       .finally(() => setChecked(true));
  }, [token]);

  if (!token) return <Navigate to="/login" />;
  if (!checked) return null;
  if (locked && location.pathname !== '/locked') return <Navigate to="/locked" />;
  return children;
};

function App() {
  return (
    <Router>
      <div className="min-h-screen font-sans">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/daily" element={<PrivateRoute><Daily /></PrivateRoute>} />
          <Route path="/leaderboard" element={<PrivateRoute><Leaderboard /></PrivateRoute>} />
          <Route path="/profile" element={<PrivateRoute><Profile /></PrivateRoute>} />
          <Route path="/locked" element={<PrivateRoute><Locked /></PrivateRoute>} />
          <Route path="/" element={<Navigate to="/dashboard" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
