import React from 'react';

import '../styles/LoginPage.css'
import RegisterPage from './RegisterPage';
import Navbar from './Navbar';
import { Link } from 'react-router-dom';

export const LoginContext = () => {
    return (
        <>
        <div className='absolute top-[100px] left-0 right-0 flex flex-col items-center justify-center gap-4 pointer-events-none mb-8'>
            <h1 className='text-4xl md:text-5xl font-bold text-white text-center px-4'>Let's get you hired.</h1>
            <h5 className='text-lg md:text-xl text-gray-400 text-center px-4'>Apply to thousands of jobs in one-click and track your status.</h5>
        </div>
        </>
    );
}

const LoginPage: React.FC = () => {
    return (
        <>
        <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center">
            <div className="w-full max-w-md p-6 mt-[200px]"> {/* Added mt-32 for top margin */}
                <div className="bg-sky-100 rounded-lg shadow-xl p-8">
                    <form className="space-y-6 h-[300px]">
                        <div>
                            <h2 className="text-2xl font-bold mb-8 text-center">Login</h2>
                            <div className="space-y-4">
                                <div>
                                    <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
                                    <input
                                        type="email"
                                        id="email"
                                        name="email"
                                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                    />
                                </div>
                                <div>
                                    <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
                                    <input
                                        type="password"
                                        id="password"
                                        name="password"
                                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                    />
                                </div>
                            </div>
                            <div className="mt-6 space-y-4">
                                <div className="text-right">
                                    <Link to="/forgot" className="text-sm text-blue-600 hover:text-blue-500">
                                        Forgot your password?
                                    </Link>
                                </div>
                                <button
                                    type="submit"
                                    className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                                >
                                    Login
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        <LoginContext />
        </>
    );
};

export default LoginPage;