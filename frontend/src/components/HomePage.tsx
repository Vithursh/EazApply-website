import React, { useEffect } from 'react';

import Navbar from './Navbar';
import { Link, Navigate } from 'react-router-dom';
import '../styles/HomePage.css'
import { useNavigate } from 'react-router-dom';

const HomePage: React.FC = () => {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate('/register');
    }

    useEffect(() => {
        const content = document.querySelector('.content');
        if (content) {
          // This will add the class to fade in the content after the component mounts
          content.classList.add('content-loaded');
        }
      }, []);    

    return (
        <div className='content'>
            <div className="bg-gray-900 text-white min-h-screen flex items-center">
                <h1 className="main-header">Automate Applying To<br></br>Jobs With EazApply</h1>
                <p className='about-website'>EazApply is a tool used to help you apply to jobs effortlessly using<br></br>artificial intelligence. <i>"All it takes is a click"</i></p>
                <button onClick={handleClick} className="bg-blue-600 text-white font-bold py-2 px-4 rounded button-position">Get Started</button>
            </div>
        </div>
    );
};
export default HomePage;