import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import { BsArrowRight } from "react-icons/bs";
import { useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import '../../styles/SkillsEnjoyWorkingWithPage.css'

const SkillsEnjoyWorkingWithPage: React.FC = () => {

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

    const goToNextPage = () => {
      if (isClicked.includes(true)) {
        navigate('/survey/minimum-expected-salary');
      } else {
        notify("You must select at least one");
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

    const [inputValue, setInputValue] = useState('');

    const addSkill = (event: React.FormEvent, value: string) => {
      event.preventDefault();
      if (value == "") {
        notify("You must type in a skill");
      } else {
        setButtonLabels(prevLabels => [...prevLabels, value]);
        console.log("Length after", lengthOfArray);
        isClicked[lengthOfArray] = true;
      }
    };  

    return (
      <>
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-800 text-white">
          <div className="text-center">
            <br></br>
            <h1 className="text-4xl mb-4">Job Preference Test</h1>
            <h2 className="text-2xl mb-2">What skills do you have or enjoy working with?</h2>
            <p>Question 7/8</p>
           
            <form className="max-w-lg mx-auto">
                <div className="flex">
                    <label htmlFor="search-dropdown" className="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Your Email</label>
                    <div className="relative">
                      <button onClick={toggleMenu} id="dropdown-button" data-dropdown-toggle="dropdown" className="dropdown-button flex-shrink-0 z-10 inline-flex items-center py-2.5 px-4 text-sm font-medium text-center text-gray-900 bg-gray-100 border border-gray-300 rounded-s-lg hover:bg-gray-200 focus:ring-4 focus:outline-none focus:ring-gray-100 dark:bg-gray-700 dark:hover:bg-gray-600 dark:focus:ring-gray-700 dark:text-white dark:border-gray-600" type="button">All categories <svg className="w-2.5 h-2.5 ms-2.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/>
                      </svg>
                      </button>
                      <div id="dropdown" className={`absolute z-10 ${isMenuOpen ? '' : 'hidden'} bg-white divide-y divide-gray-100 rounded-lg shadow w-44 dark:bg-gray-700`}>
                        {isMenuOpen && (
                          <ul className="py-2 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="dropdown-button">
                            <li><button type="button" className="inline-flex w-full px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Mockups</button></li>
                            <li><button type="button" className="inline-flex w-full px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Templates</button></li>
                            <li><button type="button" className="inline-flex w-full px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Design</button></li>
                            <li><button type="button" className="inline-flex w-full px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Logos</button></li>
                          </ul>
                        )}
                      </div>
                    </div>

                    <div className="relative w-full">
                        <input type="search" value={inputValue} onChange={e => setInputValue(e.target.value)} id="search-dropdown" className="search-bar block p-2.5 w-full z-20 text-sm text-gray-900 bg-gray-50 rounded-e-lg border-s-gray-50 border-s-2 border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-s-gray-700  dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:border-blue-500" placeholder="Search Mockups, Logos, Design Templates..." required />
                        <button type="submit" onClick={(event) => addSkill(event, inputValue)} className="absolute top-0 end-0 p-2.5 text-sm font-medium h-full text-white bg-blue-700 rounded-e-lg border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                            <svg className="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
                            </svg>
                            <span className="sr-only">Search</span>
                        </button>
                    </div>
                </div>
            </form>

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

export default SkillsEnjoyWorkingWithPage;