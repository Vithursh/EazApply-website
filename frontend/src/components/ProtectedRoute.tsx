import { Navigate, Outlet } from 'react-router-dom';
import { useEffect, useState } from 'react';
// import { useAuth } from './useAuth'; // Custom hook to get auth status
import { supabase } from '../utils/supabaseClient';
import LoadingScreen from './LoadingScreen';

function ProtectedRoutes() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Listen for auth state changes in real-time
        const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
            console.log("Auth state changed:", event);
            if (session) {
                console.log("User is logged in!!!");
                console.log("Session details:", session);
                setIsAuthenticated(true);
            } else {
                console.log("User is not logged in!!!");
                console.log("Session details:", session);
                setIsAuthenticated(false);
            }
            setIsLoading(false);
        });

        // Cleanup subscription on unmount
        return () => subscription?.unsubscribe();
    }, []);

    // Prevent the redirect until loading is finished
    if (isLoading) {
        return <LoadingScreen />;
    }

    // If the user is authenticated, render the child routes using <Outlet />
    // Otherwise, redirect them to the login page using <Navigate />
    return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};

export default ProtectedRoutes;