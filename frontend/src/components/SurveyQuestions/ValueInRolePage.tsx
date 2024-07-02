import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import { BsArrowRight } from "react-icons/bs";
import { useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import axios from 'axios';

const buttonLabels = ['Diversity & Inclusion', 'Impactful Work', 'Innovation & Tech', 'Mentorship & Career Development', 'Progressive Leadership', 'Recognition & Reward', 'Role Mobility', 'Social Responsibility & Sustainability', 'Transparency & Communication', 'Work-life balance'];

let lengthOfArray = buttonLabels.length;

const ValueInRolePage: React.FC = () => {
    const navigate = useNavigate();
    const [isClicked, setIsClicked] = useState(Array(buttonLabels.length).fill(false));

    // Initialize state variables for username, email, and password with empty strings
    const [option, setUsername] = useState('');
    // const [email, setEmail] = useState('');
    // const [password, setPassword] = useState('');

    const handleClick = (index: number) => {
      const newIsClicked = [...isClicked];
      newIsClicked[index] = !newIsClicked[index];
      setIsClicked(newIsClicked);
      if (newIsClicked[index])
        console.log(buttonLabels[index]);
    };

    const notify = (message : string) => {
      toast(message, {
        position: "top-center",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: false,
        draggable: true,
        progress: undefined,
      });
    };

    // for (let i = 0; i < lengthOfArray; i++) {
    //   if (isClicked[i] == true) {
    //     console.log(buttonLabels[i], "is getting put into the new array");
    //     console.log(isClicked[i]);
    //     handleSubmit(event, buttonLabels[i]);
    //     console.log("Sending data to the backend");
    //   }
    // }

    const goToNextPage = async () => {
      // Adds all of the words that the user selected into the "clickedLabels" array 
      const clickedLabels = buttonLabels.filter((_, index) => isClicked[index]);
    
      if (clickedLabels.length > 0 && clickedLabels.length < 4) {
        console.log(clickedLabels.length);
        try {
          const response = await axios.post('http://localhost:5000/survey/value-in-role', {
            option: clickedLabels
          }, {
            headers: {
              'Content-Type': 'application/json',
            },
            withCredentials: true,
          });
    
          const result = response.data;
          if (response.status === 200) {
            alert(result.message);
          } else {
            alert(result.error);
          }
    
          navigate('/survey/roles-interested-in');
        } catch (error) {
          console.error(`Error: ${error}`);
        }
      } else if (clickedLabels.length > 3) {
        notify("You can't select more than 3");
      } else {
        notify("You must select at least one");
      }
    };        

    return (
      <>
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-800 text-white">
          <div className="text-center">
            <h1 className="text-4xl mb-4">Job Preference Test</h1>
            <h2 className="text-2xl mb-2">What do you value in a new role?</h2>
            <p>Select up to 3</p>
            <p>Question 1/8</p>
            <div className="grid grid-cols-3 gap-4 mt-8">
              {buttonLabels.map((label, index) => (
                <div 
                  key={index} 
                  onClick={() => handleClick(index)} 
                  className={`bg-gray-700 p-4 rounded hover:bg-sky-700 ${isClicked[index] ? 'bg-sky-700' : 'bg-blue-500'}`}
                >
                  <button>{label}</button>
                </div>
              ))}
            </div>
            <button onClick={goToNextPage} className="mt-8 w-[200px] py-2 bg-blue-500 text-white rounded flex items-center justify-center mx-auto hover:bg-sky-700">
              Save and Continue 
              <BsArrowRight className="ml-2" size={20}/>
            </button>
          </div>
        </div>
        <ToastContainer theme="dark" />
      </>
    );
};    

export default ValueInRolePage;