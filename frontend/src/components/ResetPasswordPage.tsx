import React from 'react';

import '../styles/ResetPasswordPage.css'
import RegisterPage from './RegisterPage';
import Navbar from './Navbar';
import { Link } from 'react-router-dom';

export const ResetPasswordContext = () => {
    return (
        <>
        <div className='fixed top-20 left-0 right-0 flex flex-col items-center justify-center gap-4 pointer-events-none'>
            <h1 className='text-5xl font-bold text-white'>Need help logging in?</h1>
            <h5 className='text-xl text-gray-400'>Type in your email and we will send you a password reset link.</h5>
        </div>
        </>
    );
}

const ResetPasswordPage: React.FC = () => {
    return (
        <>
        <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center">
            <div className="w-full max-w-md p-6 mt-[200px]"> {/* Added mt-32 for top margin */}
                <div className="bg-sky-100 rounded-lg shadow-xl p-8">
                    <form className="space-y-6 h-[200px]">
                        <div>
                            <h2 className="text-2xl font-bold mb-8 text-center">Reset Password</h2>
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
                            </div>
                            <div className="mt-6 space-y-4">
                                <button
                                    type="submit"
                                    className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                                >
                                    Reset Password
                                </button>
                                <div className="text-center">
                                    <Link to="/register" className="text-sm text-blue-600 hover:text-blue-500">
                                        Don't have an account?
                                    </Link>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        <ResetPasswordContext />
        </>
    );
};

export default ResetPasswordPage;