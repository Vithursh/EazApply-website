![](https://github.com/Vithursh/EazApply-website/blob/236dd64ff4f92aabd88bc755ec111058416b3c2f/EazApply.png)

## Description
---

Eazapply is a website designed to help users find jobs based on their educational background, qualifications, and job preferences. This is achieved through a survey that the user fills out. The survey asks eight unique questions, each addressing a specific aspect of a job.

---

## Inspiration

---

My inspiration to create this project came from job boards like LinkedIn and Indeed. One common issue I noticed with these job boards is they recommend the same jobs even though the user has already applied to them. Additionally, my fascination with search engines also motivated me to create this project. As a kid, I found it interesting how search engines could store millions of web pages and retrieve them when users searched for certain topics. This led me to the idea of creating a website that addresses the issues people face with job boards while also developing my own recommendation engine that utilizes the same architecture as a search engine and specializes in retrieving job applications.

## Table of Contents

- Components
- Features
- Installation

## Components

- #### Backend (recommendation engine)
  - **Web crawler** (written in Python)
    - Crawls web pages to gather data by following each link of a website using the BFS algorithm
    - Handles HTML pages
    - Respects `robots.txt` rules
    - Ensures not to overload each website by using a rate-limiting algorithm known as token bucket
  - **Indexer** (written in C++)
    - Processes and stores the crawled data in an SQLite database using an inverted index schema
    - Creates an index for fast word retrieval, which helps the filtering system retrieve jobs that correlate with the user's job preferences
    - Supports full-text search capabilities
  - **Filtering system** (written in C++)
    - Filters out job applications that do not correlate with the user's educational background, qualifications, and job preferences
    - Applies various criteria to refine search results
    - Ensures data quality

![](https://github.com/Vithursh/EazApply-website/blob/30da6bc9af3c44c7fb8eb2684db9fa14b1af97a9/Search-Engine-Architecture.png)

## Features
---
- Responsive design
- User authentication
- Sign in and out of the site
- Create an account
- Real-time data updates
  - Automatically displays new jobs the user is likely to get based on their qualifications

## Installation

---

#### Running locally

##### Clone the repository

##### Be sure you have Node.js >= 16 installed.

1. Clone the repository:
   ```bash
   git clone https://github.com/Vithursh/EazApply-website.git
2. Navigate to the project directory:
   ```bash
   cd EazApply-website
3. Navigate to the frontend:
   ```bash
   cd fontend
4. Start the frontend:
   ```bash
   npm start
5. Navigate to the backend by creating a new CLI window:
   ```bash
   cd backend
6. Run the backend:
   ```bash
   python3 app.py
