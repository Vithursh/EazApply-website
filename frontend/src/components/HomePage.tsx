import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from './Navbar';
import { Link } from 'react-router-dom';
import '../styles/HomePage.css'

const HomePage: React.FC = () => {
    return (
        <div className="bg-dark text-white min-vh-100 d-flex align-items-center">
            <h1 className="main-header">Automate Applying To<br></br>Jobs With EazApply</h1>
            <p className='about-website'>EazApply is a tool used to help you apply to jobs effortlessly using<br></br>artificial intelligence.</p>
            <button className="bg-blue-600 text-white font-bold py-2 px-4 rounded button-position">Get Started</button>
        </div>
    );
};
export default HomePage;