import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import '../styles/Navbar.css';

const Navbar = () => {
  // State to control the visibility of the dropdown menu
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  // Function to toggle the dropdown menu
  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <nav className="bg-gray-800 p-2 mt-0 fixed w-full z-10 top-0">
      <div className="container mx-auto flex flex-wrap items-center">
        <div className="flex w-full md:w-1/2 justify-center md:justify-start text-white font-extrabold">
          <Link className="text-white no-underline hover:text-white hover:no-underline navbar-brand" to="/home">
            EazApply Beta
          </Link>
        </div>
        <div className="flex w-full pt-2 content-center justify-between md:w-1/2 md:justify-end">
          <ul className="list-reset flex justify-between flex-1 md:flex-none items-center">
            <li className="mr-3">
              <Link className="inline-block py-2 px-4 text-white no-underline nav-link nav-item" to="/premium">Premium</Link>
            </li>
            {/* Uncomment the below line if you have a login route */}
            {/* <li className="mr-3">
              <Link className="inline-block py-2 px-4 text-white no-underline nav-link" to="/login">Login</Link>
            </li> */}
            <li className="mr-3">
              <Link className="inline-block py-2 px-4 text-white no-underline nav-link nav-item" to="/dashboard">Dashboard</Link>
            </li>
            <li className="mr-3">
              <Link className="inline-block py-2 px-4 text-white no-underline nav-link nav-item" to="/register">Sign up</Link>
            </li>
            <li className="mr-3">
              <a className="inline-block py-2 px-4 text-white no-underline nav-link">|</a>
            </li>
            <li className="mr-3">
              <div className="relative inline-block">
                <button onClick={toggleMenu} className="inline-flex items-center text-gray-200 hover:text-white position-menu nav-item">
                  <AccountCircleIcon fontSize="large"/>
                  <span className="ml-1 nav-link">Profile</span>
                  <svg className="fill-current h-4 w-4 mt-1 ml-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M5 6l5 5 5-5z"/></svg>
                </button>
                {/* Conditionally render the dropdown menu based on isMenuOpen state */}
                {isMenuOpen && (
                  <ul className="absolute right-0 top-0 mt-12 p-2 bg-white border rounded shadow-lg me-custom">
                    <li><a className="block px-4 py-2 text-gray-800 hover:bg-indigo-500 hover:text-white no-underline hover:no-underline" href="#">Account</a></li>
                    <li><a className="block px-4 py-2 text-gray-800 hover:bg-indigo-500 hover:text-white no-underline hover:no-underline" href="#">Sign out</a></li>
                  </ul>
                )}
              </div>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;