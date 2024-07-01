import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import { Link } from 'react-router-dom';
import '../../styles/SurveyPage.css'
import { BsArrowRight } from "react-icons/bs";
import { useNavigate } from 'react-router-dom';

const SurveyPage: React.FC = () => {

    const navigate = useNavigate();

    const goToNextPage= () => {
        navigate('/survey/value-in-role');
    }

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-800 text-white">
          <div className="text-center">
            <img className="mb-4 move-pic-right" src='../../../image/Survey.png' width='500' height='300'></img>
            <h1 className="text-4xl mb-4">EazApply Survey</h1>
            <p className="text-2xl mb-2">In order to receive the most suitable job recommendations,<br></br>it is essential that you complete a survey. This survey will help <br></br>us understand your skills, interests, and career goals better,<br></br> enabling us to match you with the best possible job opportunities.</p>
            <p>This survey will contain 8 questions. Click "Continue" to proceed</p>
            <button onClick={goToNextPage} className="mt-8 w-[200px] py-2 bg-blue-500 text-white rounded flex items-center justify-center mx-auto hover:bg-sky-700">
              Continue 
              <BsArrowRight className="ml-2" size={20}/>
            </button>
          </div>
        </div>
      );
    };    

export default SurveyPage;