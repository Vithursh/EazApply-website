import React, {useState, useEffect} from 'react';

import '../styles/RegisterPage.css'
// import LoginPage from './LoginPage';
// import Navbar from './Navbar';
import { Link } from 'react-router-dom';
import axios from 'axios';
// import { fetchData } from '@/utils/fetchData';

//
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export const RegisterContext = () => {
    return (
        <>
        <div className='fixed top-20 left-0 right-0 flex flex-col items-center justify-center gap-4 pointer-events-none'>
            <h1 className='text-5xl font-bold text-white'>Register with us today</h1>
            <h5 className='text-xl text-gray-400'>Quickly find and apply to thousands of jobs in one-click.</h5>
        </div>
        </>
    );
}

const RegisterPage: React.FC = () => {
    
    // Initialize state variables for username, email, and password with empty strings
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    // Notifcation 
    const notify = (message : string) => {
        toast(message, {
          position: "top-center",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
        });
    };

    // Define an asynchronous function to handle form submission
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        // Prevent the default form submission behavior
        event.preventDefault();
        
        // Send a POST request to the /register endpoint
        try {
            const response = await axios.post('http://localhost:5000/register', {
                username,
                email,
                password
            }, {
                headers: {
                    'Content-Type': 'application/json',  // Set the content type of the request body
                },
                withCredentials: true,  // Add this line
            });
            
            // The response data is already parsed as JSON
            const result = response.data;
            if (response.status === 200) {
                // If the request was successful, display the message from the server
                // alert(result.message);
                notify(result.message);
            } else {
                // If the request failed, display the error from the server
                notify(result.error);
            }
        } catch (error) {
            console.error(`Error: ${error}`);
        }
    };    

    return (
        <>
        <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center">
            <div className="w-full max-w-md p-6 mt-[200px]"> {/* Added mt-32 for top margin */}
                <div className="bg-sky-100 rounded-lg shadow-xl p-8">
                    <form onSubmit={handleSubmit} className="space-y-6 h-[350px]">
                        <div>
                            <h2 className="text-2xl font-bold mb-8 text-center">Register</h2>
                            <div className="space-y-4">
                                <div>
                                    <label htmlFor="fname" className="block text-sm font-medium text-gray-700">Name</label>
                                    <input
                                        type="text"
                                        value={username}
                                        onChange={(e) => setUsername(e.target.value)}
                                        id="fname"
                                        name="fname"
                                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                    />
                                </div>
                                <div>
                                    <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
                                    <input
                                        type="email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        id="email"
                                        name="email"
                                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                    />
                                </div>
                                <div>
                                    <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
                                    <input
                                        type="password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        id="password"
                                        name="password"
                                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                    />
                                </div>
                            </div>
                            <div className="mt-6 space-y-4">
                                <button
                                    type="submit"
                                    className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                                >
                                    Register
                                </button>
                                <div>
                                    <Link to="/login" className="text-sm text-blue-600 hover:text-blue-500">
                                        Already have an account?
                                    </Link>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        <RegisterContext />
        <ToastContainer theme="dark" />
        </>
    );
};

export default RegisterPage;