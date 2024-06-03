import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/DashboardPage.css'
import { Link, Navigate } from 'react-router-dom';
import '../styles/HomePage.css'
import { useNavigate } from 'react-router-dom';
import icon from "../../image/icon.png"
import { BsArrowLeftShort, BsFillPersonFill, BsFillHouseDoorFill} from "react-icons/bs";

export const Icon = ({ className, size }: { className?: string, size?: string }) => {
    // 'large' corresponds to '48px', otherwise default to '24px'
    const iconSize = size === 'large' ? '48px' : '50px';
    return (
      <img
        src={icon}
        alt="Icon"
        style={{ width: iconSize, height: iconSize, minWidth: iconSize }}
        className={`inline ${className}`}
      />
    );
  };  

export const DashboardContext = () => {
    return (
        <>
        <div className='absolute inset-0 flex items-center justify-center z-0 pointer-events-none'>
            <h1 className='welcome-message'>Welcome back Vithursh!</h1>
        </div>
        <div className='absolute inset-0 flex items-center justify-center z-0 pointer-events-none'>
            <h5 className='job-label text-gray-500'>See your matched jobs: </h5>
        </div>
        
        <div style={{ width: '410px', height: '250px' }} className="absolute top-44 right-80 inset-0 mx-auto bg-white rounded-xl shadow-md overflow-hidden md:max-w-2xl m-3">
            <div className="md:flex">
                <div className="md:flex-shrink-0">
                    <img className="h-full w-full object-cover md:w-18" src="/path-to-your-image.jpg" alt="image"/>
                </div>
            <div className="mt-2">
                <div className="mt-1 move-header-right uppercase tracking-wide text-sm text-indigo-500 font-semibold">Job Type</div>
                <a href="#" className="block mt-1 move-left text-lg leading-tight font-medium text-black hover:underline">Job title</a>
                <p className="mt-20 move-right text-gray-500">Job description goes here.</p>
            </div>
            </div>
        </div>
        </>
    );
}

const DashboardPage: React.FC = () => {

    // State to control the visibility of the dropdown menu
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    // Function to toggle the dropdown menu
    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    };

    const [open, setOpen] = useState(true);

    return (
        <>
    <div className='bg-dark text-white min-vh-100 d-flex align-items-center flex'>
        <div className={`bg-gray-800 h-screen pt-8 pl-0 ${open ? "w-72 pr-5 pb-5" : "w-20 pr-5 pb-5"} duration-300 relative flex items-start`}>
            <div className="flex flex-col">
                <Link className="inline-flex items-center py-2 px-4 text-white no-underline" to="/home">
                    <Icon className={`duration-500 ${open && "rotate-[360deg]"}`} /> {open ? <span className='transition-opacity duration-300 opacity-100 company-title'>azApply</span> : <span className='transition-opacity duration-300 opacity-0'>azApply</span>}
                </Link>

                <button>
                    <div className={`flex items-center py-2 px-4 text-white no-underline rounded-md ${open ? "bg-light-blue" : "bg-light-white"} mt-6 px-4 py-2 transition-colors duration-500 nav-item`}>
                        <BsFillHouseDoorFill className={`duration-500 ${open && "rotate-[360deg]"} text-white ml-2`} size="30px" /> {open ? <span className='transition-opacity duration-300 opacity-100 categories'>Dashboard</span> : <span className='transition-opacity duration-300 opacity-0'>azApply</span>}
                    </div>
                </button>

                <div className="fixed bottom-0 left-0 inline-block text-left">
                <button onClick={toggleMenu}>
                    <div className={`flex items-center py-2 px-4 text-white no-underline rounded-md ${open ? "bg-light-blue" : "bg-light-white"} mt-6 px-4 py-2 transition-colors duration-500 nav-item`}>
                    <BsFillPersonFill className={`duration-500 ${open && "rotate-[360deg]"} text-white ml-2`} size="35px"/> {open ? <span className='transition-opacity duration-300 opacity-100 categories'>Users Name</span> : <span className='transition-opacity duration-300 opacity-0'>azApply</span>}
                    </div>
                </button>
                <div className={`origin-top-right absolute right-0 bottom-full mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 ${isMenuOpen ? 'block' : 'hidden'}`}>
                    <div className="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
                    <a href="#" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem">Account settings</a>
                    <a href="#" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem">Support</a>
                    <a href="#" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem">License</a>
                    <a href="/login" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem">Sign out</a>
                    </div>
                </div>
                </div>
                
            </div>
            <BsArrowLeftShort className={`bg-black text-dark-purple text-3xl rounded-full absolute -right-3 top-9 cursor-pointer ${!open && "rotate-180"}`} onClick={() => setOpen(!open)} />
        </div>
    </div>
    <DashboardContext />
    </>
    );
};

export default DashboardPage;