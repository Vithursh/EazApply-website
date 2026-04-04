import { useState, useEffect } from 'react'
import { Route, Routes, useLocation, useNavigate, Navigate, Router, BrowserRouter } from 'react-router-dom';
import LoginPage from "./components/LoginPage";
import RegisterPage from "./components/RegisterPage";
import Navbar from './components/Navbar';
import HomePage from './components/HomePage';
import ResetPasswordPage from './components/ResetPasswordPage';
import DashboardPage from './components/DashboardPage';
import { BasicPlan, ElitePlan, StandardPlan } from './components/PremiumPage';
import ProtectedRoute from './components/ProtectedRoute';
import type { Session } from '@supabase/supabase-js';

// Survey pages
import SurveyPage from './components/SurveyQuestions/SurveyPage';
import ValueInRolePage from './components/SurveyQuestions/ValueInRolePage';
import RolesInterestedInPage from './components/SurveyQuestions/RolesInterestedInPage';
import LikeToWorkPage from './components/SurveyQuestions/LikeToWorkPage';
import LevelOfExperiencePage from './components/SurveyQuestions/LevelOfExperiencePage';
import CompanySizePage from './components/SurveyQuestions/CompanySizePage';
import IndustriesExcitedInPage from './components/SurveyQuestions/IndustriesExcitedInPage';
import SkillsEnjoyWorkingWithPage from './components/SurveyQuestions/SkillsEnjoyWorkingWithPage';
import MinimumExpectedSalaryPage from './components/SurveyQuestions/MinimumExpectedSalaryPage';

// Supabase
import { supabase } from './utils/supabaseClient';

function PremiumPage() {
  return (
    <div>
      <BasicPlan />
      <StandardPlan />
      <ElitePlan />
    </div>
  );
}

function AuthStateListener() {
  const navigate = useNavigate();

  useEffect(() => {
    const { data: authListener } = supabase.auth.onAuthStateChange((event, session) => {
      console.log('The session for App is:', session);
      // If user is logged in and tries to access login or register page, redirect to dashboard
      if (session && (window.location.pathname === '/login' || window.location.pathname === '/register' || window.location.pathname === '/')) {
        navigate('/dashboard');
      }
      // If user is logged out and tries to access a protected route, redirect to homepage
      if (!session && window.location.pathname !== '/login' && window.location.pathname !== '/register' && window.location.pathname !== '/forgot') {
        navigate('/');
      }
    });

    return () => {
      authListener.subscription.unsubscribe();
    };
  }, [navigate]);

  return null;
}

function App() {
  const location = useLocation();

  return (
    <>
      <AuthStateListener />
      {location.pathname !== '/dashboard' &&
       !location.pathname.startsWith('/survey') &&
       <Navbar />}
          {/* <BrowserRouter> */}
            <Routes>
              {/* Public routes */}
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/" element={<HomePage />} />
              <Route path="/premium" element={<PremiumPage />} />
              <Route path="/forgot" element={<ResetPasswordPage />} />

              {/* Protected routes wrapped in the ProtectedRoute component */}
              <Route element={<ProtectedRoute />}>
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/survey" element={<SurveyPage />} />
                <Route path="/survey/value-in-role" element={<ValueInRolePage />} />
                <Route path="/survey/roles-interested-in" element={<RolesInterestedInPage />} />
                <Route path="/survey/like-to-work" element={<LikeToWorkPage />} />
                <Route path="/survey/level-of-experience" element={<LevelOfExperiencePage />} />
                <Route path="/survey/company-size" element={<CompanySizePage />} />
                <Route path="/survey/industries-excited-in" element={<IndustriesExcitedInPage />} />
                <Route path="/survey/skills-enjoy-working-with" element={<SkillsEnjoyWorkingWithPage />} />
                <Route path="/survey/minimum-expected-salary" element={<MinimumExpectedSalaryPage />} />
              </Route>

            </Routes>
          {/* </BrowserRouter> */}
    </>
  );
}

export default App;