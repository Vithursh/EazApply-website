import React from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation} from 'react-router-dom';
import LoginPage from "./components/LoginPage";
import RegisterPage from "./components/RegisterPage";
import Navbar from './components/Navbar';
import HomePage from './components/HomePage';
import ResetPasswordPage from './components/ResetPasswordPage';
import DashboardPage from './components/DashboardPage';
import { BasicPlan, ElitePlan, StandardPlan } from './components/PremiumPage';
import './index.css';

function PremiumPage() {
  return (
    <div>
      <BasicPlan />
      <StandardPlan />
      <ElitePlan />
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="*" element={<Layout />} />
      </Routes>
    </Router>
  );
}

function Layout() {
  const location = useLocation();

  return (
    <div>
      {location.pathname !== '/dashboard' && <Navbar />}
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/premium" element={<PremiumPage />} />
        <Route path="/forgot" element={<ResetPasswordPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
    </div>
  );
}

export default App;