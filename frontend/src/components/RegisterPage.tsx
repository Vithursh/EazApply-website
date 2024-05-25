import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/RegisterPage.css'
import LoginPage from './LoginPage';
import Navbar from './Navbar';
import { Link } from 'react-router-dom';

const RegisterPage: React.FC = () => {
    return (
        <div className="bg-dark text-dark min-vh-100 d-flex align-items-center">
            <div className="container">
                <div className="row justify-content-center">
                    <div className="col-md-6">
                        <div className="card">
                            <div className="card-body">
                                <form className="dark-blue">
                                    <div className="form-group">
                                        <label className="register-label">Register</label>
                                        <br></br>
                                        <label htmlFor="fname">Name</label>
                                        <input type="text" id="fname" name="fname" className="form-control custom-width"/>
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
                                    <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded btn-primary">Register</button>
                                    <br></br>
                                    <br></br>
                                    <Link to='/login'>Already have an account?</Link>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RegisterPage;