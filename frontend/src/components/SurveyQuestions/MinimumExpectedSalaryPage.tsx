import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import { BsArrowRight } from "react-icons/bs";
import { useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import '../../styles/MinimumExpectedSalaryPage.css'

const MinimumExpectedSalaryPage: React.FC = () => {

    const [buttonLabels, setButtonLabels] = useState([
      'Adobe Illustrator', 'Business Analytics', 'Excel/Numbers/Sheets', 
      'MailChimp', 'MATLAB', 'Operations Research', 
      'SEO', 'Zendesk'
    ]);

    let lengthOfArray = buttonLabels.length;

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

    const [value, setValue] = useState(150);

    const goToNextPage = () => {
      if (value != 0) {
        navigate('/register');
      } else {
        notify("You must select at least 1K");
      }
      for (let i = 0; i < lengthOfArray; i++) {
        if (isClicked[i] == true) {
          console.log(buttonLabels[i], "is getting put into the new array");
          console.log(isClicked[i]); 
        }
      }
    }

    // State to control the visibility of the dropdown menu
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    // Function to toggle the dropdown menu
    const toggleMenu = () => {
      setIsMenuOpen(!isMenuOpen);
    };

    return (
      <>
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-800 text-white">
          <div className="text-center">
            <br></br>
            <h1 className="text-4xl mb-4">Job Preference Test</h1>
            <h2 className="text-2xl mb-2">What is your minimum expected salary?</h2>
            <p>Question 8/8</p>

                <div className="space-y-8">
                    <div>
                        <p className="text-gray-500">We'll only use this to match you with jobs and will not share this data.</p>
                    </div>
                    <div>
                        <label htmlFor="salary" className="block text-sm text">
                        At least ${value}K USD
                        </label>
                        <br></br>
                        <input
                        type="range"
                        id="salary"
                        name="salary"
                        min="0"
                        max="300"
                        value={value}
                        onChange={event => setValue(Number(event.target.value))}
                        className="mt-1 block w-full h-5 rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0"
                        />
                    </div>
                </div>

            <button onClick={goToNextPage} className="mt-8 w-[200px] py-2 bg-blue-500 text-white rounded flex items-center justify-center mx-auto hover:bg-sky-700">
              Finish 
              <BsArrowRight className="ml-2" size={20}/>
            </button>
            <br></br>
          </div>
        </div>
        <ToastContainer theme="dark" />
      </>
    );
};    

export default MinimumExpectedSalaryPage;