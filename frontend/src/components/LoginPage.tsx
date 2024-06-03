import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/LoginPage.css'
import RegisterPage from './RegisterPage';
import Navbar from './Navbar';
import { Link } from 'react-router-dom';

export const LoginContext = () => {
    return (
        <>
        <div className='absolute inset-0 flex items-center justify-center z-0 pointer-events-none'>
            <h1 className='register-message'>Let's get you hired.</h1>
        </div>
        <div className='absolute inset-0 flex items-center justify-center z-0 pointer-events-none'>
            <h5 className='little-header text-gray-500'>Apply to thousands of jobs in one-click and track your status.</h5>
        </div>
        </>
    );
}

const LoginPage: React.FC = () => {
    return (
        <>
        <div className="bg-dark text-dark min-vh-100 d-flex align-items-center">
            <div className="container">
                <div className="row justify-content-center">
                    <div className="col-md-6">
                        <div className="card border-color">
                            <div className="card-body">
                                <form className="dark-blue">
                                    <div className="form-group">
                                        <label className="register-label">Login</label>
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="lname">Email</label>
                                        <input type="text" id="lname" name="lname" className="form-control custom-width"/>
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="lname">Password</label>
                                        <input type="text" id="lname" name="lname" className="form-control custom-width"/>
                                    </div>
                                    <Link className='forgot-password' to='/forgot'>Forgot your password?</Link>
                                    <br></br>
                                    <br></br>
                                    <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded btn-primary">Login</button>
                                    <br></br>
                                    <br></br>
                                    {/* <Link to='/register'>Don't have an account?</Link> */}
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <LoginContext/>
        </>
    );
};

export default LoginPage;