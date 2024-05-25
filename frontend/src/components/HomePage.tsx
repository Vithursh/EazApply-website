import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from './Navbar';
import { Link, Navigate } from 'react-router-dom';
import '../styles/HomePage.css'
import { useNavigate } from 'react-router-dom';

const HomePage: React.FC = () => {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate('/register');
    }

    return (
        <div className="bg-dark text-white min-vh-100 d-flex align-items-center">
            <h1 className="main-header">Automate Applying To<br></br>Jobs With EazApply</h1>
            <p className='about-website'>EazApply is a tool used to help you apply to jobs effortlessly using<br></br>artificial intelligence. "All it takes is a click"</p>
            <button onClick={handleClick} className="bg-blue-600 text-white font-bold py-2 px-4 rounded button-position">Get Started</button>
        </div>
    );
};
export default HomePage;