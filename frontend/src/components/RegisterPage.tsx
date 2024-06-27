import React, {useState, useEffect} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../styles/RegisterPage.css'
import LoginPage from './LoginPage';
import Navbar from './Navbar';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { fetchData } from '@/utils/fetchData';

export const RegisterContext = () => {
    return (
        <>
        <div className='absolute inset-0 flex items-center justify-center z-0 pointer-events-none'>
            <h1 className='register-message'>Register with us today</h1>
        </div>
        <div className='absolute inset-0 flex items-center justify-center z-0 pointer-events-none'>
            <h5 className='little-header text-gray-500'>Quickly find and apply to thousands of jobs in one-click.</h5>
        </div>
        </>
    );
}

const RegisterPage: React.FC = () => {
    
    // Initialize state variables for username, email, and password with empty strings
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    // Vaildates email
    // function isValidEmail(email: string) : boolean {
    //     // Define a regular expression pattern for email validation.
    //     const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    //     const tableName = 'users';
    //     console.log(email);

    //     fetchData(tableName)
    //     .then(data => {
    //         if (data !== null) {
    //         console.log('Data:', data);
    //         } else {
    //             console.log("There is no data in the", tableName, "table.")
    //         }
    //     });

    //     return pattern.test(email);
    // }

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
                alert(result.message);
            } else {
                // If the request failed, display the error from the server
                alert(result.error);
                console.log("DID NOT WORK!!!");
            }
        } catch (error) {
            console.error(`Error: ${error}`);
        }
    };    

    return (
        <>
        <div className="bg-dark text-dark min-vh-100 d-flex align-items-center">
            <div className="container">
                <div className="row justify-content-center">
                    <div className="col-md-6">
                        <div className="card">
                            <div className="card-body">
                                <form className="dark-blue" onSubmit={handleSubmit}>
                                    <div className="form-group">
                                        <label className="register-label">Register</label>
                                        <br></br>
                                        <label htmlFor="fname">Name</label>
                                        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} id="fname" name="fname" className="form-control custom-width"/>
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="lname">Email</label>
                                        <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} id="lname" name="lname" className="form-control custom-width"/>
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="lname">Password</label>
                                        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} id="lname" name="lname" className="form-control custom-width"/>
                                    </div>
                                    <br></br>
                                    <button type='submit' className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded btn-primary">Register</button>
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
        <RegisterContext/>
        </>
    );
};

export default RegisterPage;