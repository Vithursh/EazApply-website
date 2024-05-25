import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/ResetPasswordPage.css'
import RegisterPage from './RegisterPage';
import Navbar from './Navbar';
import { Link } from 'react-router-dom';

const ResetPasswordPage: React.FC = () => {
    return (
        <div className="bg-dark text-dark min-vh-100 d-flex align-items-center">
            <div className="container">
                <div className="row justify-content-center">
                    <div className="col-md-6">
                        <div className="card border-color">
                            <div className="card-body">
                            <h1 className='reset-password-title'>Need help logging in?</h1>
                                <form className="dark-blue form-size-reset">
                                    <div className="form-group">
                                        <label htmlFor="lname">Email</label>
                                        <input type="text" id="lname" name="lname" className="form-control custom-width"/>
                                    </div>
                                    <br></br>
                                    <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded btn-primary-reset">Reset Password</button>
                                    <br></br>
                                    <br></br>
                                    <Link className='no-account' to='/register'>Don't have an account?</Link>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ResetPasswordPage;