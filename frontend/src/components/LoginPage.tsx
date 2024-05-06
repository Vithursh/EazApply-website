import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/LoginPage.css'
import RegisterPage from './RegisterPage';
import Navbar from './Navbar';
import { Link } from 'react-router-dom';

const LoginPage: React.FC = () => {
    return (
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
                                    <br></br>
                                    <button className="btn btn-primary">Login</button>
                                    <Link to='/register'>Don't have an account?</Link>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;