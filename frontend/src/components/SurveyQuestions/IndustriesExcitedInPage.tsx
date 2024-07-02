import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import { BsArrowRight } from "react-icons/bs";
import { useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import axios from 'axios';

const buttonLabels = [
    'Aerospace', 'Automotive & Transportation', 'Consumer Goods', 
    'Consumer Software', 'Crypto & Web3', 'Cybersecurity', 
    'Data & Analytics', 'Defense', 'Design', 
    'Education Services', 'Energy', 'Enterprise Software', 
    'Entertainment', 'Financial Services', 'Fintech', 
    'Food & Agriculture', 'Government & Public Sector', 'Hardware', 
    'Healthcare', 'Industrial & Manufacturing', 'Legal', 
    'Quantitative Finance', 'Real Estate', 'Robotics & Automation', 
    'Social Impact', 'Venture Capital', 'VR & AR'
  ];

  let lengthOfArray = buttonLabels.length;

const IndustriesExcitedInPage: React.FC = () => {
    const navigate = useNavigate();
    const [isClicked, setIsClicked] = useState(Array(buttonLabels.length).fill(false));

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

    const goToNextPage = async () => {
      // Adds all of the words that the user selected into the "clickedLabels" array 
      const clickedLabels = buttonLabels.filter((_, index) => isClicked[index]);
    
      if (clickedLabels.length > 0 && clickedLabels.length < 6) {
        console.log(clickedLabels.length);
        try {
          const response = await axios.post('http://localhost:5000/survey/industries-excited-in', {
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
    
          navigate('/survey/skills-enjoy-working-with');
        } catch (error) {
          console.error(`Error: ${error}`);
        }
      } else if (clickedLabels.length > 5) {
        notify("You can't select more than 5");
      } else {
        notify("You must select at least one");
      }
    };

    return (
      <>
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-800 text-white">
          <div className="text-center">
            <br></br>
            <h1 className="text-4xl mb-4">Job Preference Test</h1>
            <h2 className="text-2xl mb-2">What industries are exciting to you?</h2>
            <p>Select up to 5</p>
            <p>Question 6/8</p>
            <div className="grid grid-cols-3 gap-4 mt-8">
              {buttonLabels.map((label, index) => (
                <div 
                  key={index} 
                  onClick={() => handleClick(index)}
                  style={{ 
                    padding: '10px 20px', 
                    borderRadius: '20px', 
                    border: 'none', 
                  }} 
                  className={`bg-gray-700 hover:bg-sky-700 ${isClicked[index] ? 'bg-sky-700' : 'bg-blue-500'}`}
                >
                  <button>{label}</button>
                </div>
              ))}
            </div>
            <button onClick={goToNextPage} className="mt-8 w-[200px] py-2 bg-blue-500 text-white rounded flex items-center justify-center mx-auto hover:bg-sky-700">
              Save and Continue 
              <BsArrowRight className="ml-2" size={20}/>
            </button>
            <br></br>
          </div>
        </div>
        <ToastContainer theme="dark" />
      </>
    );
};    

export default IndustriesExcitedInPage;