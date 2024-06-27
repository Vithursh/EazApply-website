import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Route, Routes, useLocation} from 'react-router-dom';
import LoginPage from "./components/LoginPage";
import RegisterPage from "./components/RegisterPage";
import Navbar from './components/Navbar';
import HomePage from './components/HomePage';
import ResetPasswordPage from './components/ResetPasswordPage';
import DashboardPage from './components/DashboardPage';
import { BasicPlan, ElitePlan, StandardPlan } from './components/PremiumPage';
import './index.css';

// Supabase libaries
import { createClient } from '@supabase/supabase-js'
import { Auth } from '@supabase/auth-ui-react'
import { ThemeSupa } from '@supabase/auth-ui-shared'

// Remove once you figure out how to import enviroment variables
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

function App() {

  const [session, setSession] = useState(null)

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }: any) => {
      setSession(session)
    })    

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event: any, session: any) => {
      setSession(session)
    })    

    return () => subscription.unsubscribe()
  }, [])

  return (
    <Router>
      <Routes>
        <Route path="*" element={<Layout />} />
      </Routes>
      {!session ? (
        <Auth supabaseClient={supabase} appearance={{ theme: ThemeSupa }} />
      ) : (
        <div>Logged in!</div>
      )}
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