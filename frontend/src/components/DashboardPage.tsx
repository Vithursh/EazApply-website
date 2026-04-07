import React, { useEffect, useState } from 'react';
import axios from "axios";
import '../styles/DashboardPage.css'
import { Link, Navigate, useParams } from 'react-router-dom';
import '../styles/HomePage.css'
import { useNavigate } from 'react-router-dom';
import icon from "../../image/icon.png"
import { BsArrowLeftShort } from "@react-icons/all-files/bs/BsArrowLeftShort";
import { BsFillPersonFill } from "@react-icons/all-files/bs/BsFillPersonFill";
import { BsFillHouseDoorFill } from "@react-icons/all-files/bs/BsFillHouseDoorFill";
// import type { Session } from '@supabase/supabase-js';
// import { Session } from 'inspector';
import { createBrowserSupabase as createClient } from '../utils/supabase/client';

const supabase = createClient();

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

export const JobCard = ({ job }: { job: any }) => (
//   <div className="max-w-sm rounded overflow-hidden shadow-lg">
  <div className="w-80 rounded overflow-hidden shadow-lg">
    {/* Job image (fallback to placeholder if missing) */}
    <img
      className="w-full"
      src={job.image ?? 'https://picsum.photos/seed/picsum/200/100'}
      alt={job.title ?? 'job image'}
    />

    {/* Title & description */}
    <div className="px-6 py-4">
      <div className="font-bold text-xl mb-2">
        {job.title ?? 'Untitled Position'}
      </div>
      <p className="text-gray-700 text-base">
        {job.companyName ?? 'No company name provided.'}
      </p>
      <p className="text-gray-700 text-base">
        {job.description ?? 'No description provided.'}
      </p>
    </div>

    {/* Tags (if any) */}
    {Array.isArray(job.tags) && job.tags.length > 0 && (
      <div className="px-6 pt-4 pb-2">
        {job.tags.map((tag: string, idx: number) => (
          <span
            key={idx}
            className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2"
          >
            #{tag}
          </span>
        ))}
      </div>
    )}

    {/* “Apply” button */}
    <div className="px-6 pb-4">
      <a
        href={job.url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-block bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        Apply
      </a>
    </div>
  </div>
)

export const DashboardContext = () => (
    <div className="mt-8 mb-8 self-start ml-12">
        <h1 className='text-5xl font-bold text-white'>Welcome back Vithursh!</h1>
        <h5 className='text-3xl text-gray-500'>See your matched jobs: </h5>
    </div>
);

const DashboardPage: React.FC = () => {
    // The key 'uuid' here must match the name used in your Route path (:uuid)
    const { uuid } = useParams();
    console.log("The UUID from the URL is:", uuid); // This should log the correct UUID when the component renders
    const navigate = useNavigate();
    // await supabase.auth.getUser();
    const [session, setSession] = useState<any | null>(null);

    useEffect(() => {
      const getSession = async () => {
        const userSession = await supabase.auth.getSession();
        // console.log("Current session:", userSession);
        setSession(userSession);
      };

      getSession();
    }, []);

    // State to control the visibility of the dropdown menu
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    // Function to toggle the dropdown menu
    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    };

    const [open, setOpen] = useState(true);

    const [data, setData] = useState([]);

    const handleLogout = async () => {
      // const navigate = useNavigate(); // Already declared at component level

      try {
        const { error } = await supabase.auth.signOut();

        // Manually clear common storage keys just in case
        localStorage.removeItem('sb-access-token');
        localStorage.removeItem('sb-refresh-token');
        // Or clear everything if your app doesn't need other local data
        localStorage.clear(); 

        // if (!error) {
        //   // Force a full reload to the login page to kill all background processes
        //   window.location.href = '/login';
        // }
        
      } catch (error) {
        console.error('Error signing out:', error);
        alert('Failed to sign out');
      }
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('http://localhost:5000/dashboard', { params: { userId: uuid }, withCredentials: true });
                if (response.status === 200) {
                    // Handle successful response
                    console.log("Dashboard data refreshed every 5 seconds...");
                    console.log('Dashboard data:', response.data);
                    setData(response.data);
                } else {
                    // Handle error response
                    console.log('Could not get data!!!');
                }
            } catch (error) {
                console.error('Error fetching dashboard data:', error);
            }
        };
        fetchData();

        // Refresh the data every 5 seconds
        const intervalId = setInterval(fetchData, 5000); // Fetch every 5 seconds

        return () => clearInterval(intervalId); // Cleanup on component unmount
    }, []);

    return (
        <>
        <div className="flex min-h-screen bg-gray-900 text-white">
                {/* Sidebar */}
                <aside className={`bg-gray-800 h-screen sticky top-0 pt-8 pl-0 ${open ? "w-70 pr-5 pb-5" : "w-20 pr-5 pb-5"} duration-300 relative flex flex-col items-start`}>
                    <Link className="inline-flex items-center py-2 px-4 text-white no-underline" to="/">
                        <Icon className={`-ml-1 duration-500 ${open && "rotate-[360deg]"}`} /> 
                        {open ? <span className='transition-opacity duration-300 opacity-100 company-title'>azApply</span> : <span className='transition-opacity duration-300 opacity-0'>azApply</span>}
                    </Link>
                    <button>
                        <div className={`flex items-center py-2 px-4 text-white no-underline rounded-md mt-6 px-4 py-2 transition-colors duration-500 nav-item`}>
                            <BsFillHouseDoorFill className={`-ml-0 duration-500 ${open && "rotate-[360deg]"} text-white ml-2`} size="30px" /> 
                            {open
                              ? (
                                  <span
                                    className="
                                      inline-block
                                      transition-[width,opacity]
                                      duration-300
                                      origin-left
                                      overflow-hidden
                                      w-auto
                                      opacity-100
                                      categories
                                    "
                                  >
                                    Dashboard
                                  </span>
                                )
                              : (
                                  <span
                                    className="
                                      inline-block
                                      transition-[width,opacity]
                                      duration-300
                                      origin-left
                                      overflow-hidden
                                      w-0
                                      opacity-0
                                    "
                                  >
                                    azApply
                                  </span>
                                )
                            }
                        </div>
                    </button>
                    <div className="absolute bottom-0 left-0 inline-block text-left">
                        <button onClick={toggleMenu}>
                            <div className={`flex items-center py-2 px-4 text-white no-underline rounded-md mt-6 px-4 py-2 transition-colors duration-500 nav-item`}>
                                <BsFillPersonFill className={`-ml-0 duration-500 ${open && "rotate-[360deg]"} text-white ml-2`} size="30px"/>
                                {open
                                  ? (
                                      <span
                                        className="
                                          inline-block
                                          transition-[width,opacity]
                                          duration-300
                                          origin-left
                                          overflow-hidden
                                          w-auto
                                          opacity-100
                                          categories
                                        "
                                      >
                                        User Name
                                      </span>
                                    )
                                  : (
                                      <span
                                        className="
                                          inline-block
                                          transition-[width,opacity]
                                          duration-300
                                          origin-left
                                          overflow-hidden
                                          w-0
                                          opacity-0
                                        "
                                      >
                                        azApply
                                      </span>
                                    )
                                }
                            </div>
                        </button>
                        <div className={`origin-top-right absolute left-1 bottom-full mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 ${isMenuOpen ? 'block' : 'hidden'}`}>
                            <div className="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
                                <a href="#" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem">Account settings</a>
                                {/* <a href="#" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem">Support</a> */}
                                {/* <a href="#" className="block px-4 py-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem">License</a> */}
                                <a href="/login" onClick={handleLogout} className="block px-4 py-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900" role="menuitem">{session ? 'Sign out' : 'Sign In'}</a>
                            </div>
                        </div>
                    </div>
                    <BsArrowLeftShort className={`bg-black text-dark-purple text-3xl rounded-full absolute -right-3 top-9 cursor-pointer ${!open && "rotate-180"}`} onClick={() => setOpen(!open)} />
                </aside>
                {/* Main Content */}
                <div className="flex-1 flex flex-col relative">
                    <DashboardContext />
                    <div className="flex flex-wrap gap-6 justify-center p-12">
                        {data.map((job) => (
                            <JobCard job={job} key={job.id} />
                        ))}
                    </div>
                </div>
            </div>
        </>
    );
};

export default DashboardPage;