import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'; // This will include Tailwind's styles
import { BrowserRouter } from 'react-router-dom'

// import dotenv from 'dotenv';

// dotenv.config({ path: '../../.env' });

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
)
