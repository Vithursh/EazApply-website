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
      {/* {!session ? (
        <Auth supabaseClient={supabase} appearance={{ theme: ThemeSupa }} />
      ) : (
        <div>Logged in!</div>
      )} */}
    </Router>
  );
}

function Layout() {
  const location = useLocation();

  return (
    <div>
      {location.pathname !== '/dashboard' && location.pathname !== '/survey' && location.pathname !== '/survey/value-in-role' && location.pathname !== '/survey/roles-interested-in' && location.pathname !== '/survey/like-to-work' && location.pathname !== '/survey/level-of-experience' && location.pathname !== '/survey/company-size' && location.pathname !== '/survey/industries-excited-in' && location.pathname !== '/survey/skills-enjoy-working-with' && location.pathname !== '/survey/minimum-expected-salary' && <Navbar />}
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/premium" element={<PremiumPage />} />
        <Route path="/forgot" element={<ResetPasswordPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        
        <Route path="/survey" element={<SurveyPage />}>
            // Add more routes for more questions
        </Route>
        <Route path="/survey/value-in-role" element={<ValueInRolePage />} />
        <Route path="/survey/roles-interested-in" element={<RolesInterestedInPage />} />
        <Route path="/survey/like-to-work" element={<LikeToWorkPage />} />
        <Route path="/survey/level-of-experience" element={<LevelOfExperiencePage />} />
        <Route path="/survey/company-size" element={<CompanySizePage />} />
        <Route path="/survey/industries-excited-in" element={<IndustriesExcitedInPage />} />
        <Route path="/survey/skills-enjoy-working-with" element={<SkillsEnjoyWorkingWithPage />} />
        <Route path="/survey/minimum-expected-salary" element={<MinimumExpectedSalaryPage />} />
      </Routes>
    </div>
  );
}

export default App;