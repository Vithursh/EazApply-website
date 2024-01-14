# Import the linkedin_scraper function from scraper.py
#from scraper import linkedin_scraper

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import requests
import csv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 

# Create a new web application object.
app = Flask(__name__)

# Path to the .db file that will be created
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Defines the format of the database
class data(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.String(200))
    company = db.Column(db.String(200))
    location = db.Column(db.String(200))
    applyLink = db.Column(db.String(200))

def check_if_Contains_Work_day():
    global service
    global driver
    service = Service(executable_path="/home/vithursh/Coding/EazApply/Web Scraper/chromedriver-linux64/chromedriver")
    print("\nReads chrome driver\n")
    driver = webdriver.Chrome(service=service)
    driver.get(clean_string)
    print("\nIs fetching link\n")

def read_csv_and_store_in_database(csv_filename):
    with open(csv_filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row if it exists
        db.drop_all()
        counter = 0
        with app.app_context():
            db.create_all()
            for row in csv_reader:
                global clean_string
                clean_string = row[3][2:-1]
                req = requests.get(clean_string)
                print(clean_string)

                # Checks if each link contain ".workday"
                check_if_Contains_Work_day()
                time.sleep(5)
                driver.quit()

                # Checks if each link in the database contains a "https" in it
                if "https:" in row[3]:
                    # Counting to see how much links there are
                    counter+=1
                    print("IIIIISSSSS")
                    print(counter)
                else:
                    print("\nDoes not")

                # Assuming CSV columns match the model columns
                record = data(title=row[0], company=row[1], location=row[2], applyLink=row[3])
                db.session.add(record)
            print("There are",counter,"links that contain 'https' in it")
            db.session.commit()
            
@app.route('/')
def index():
    #print("Route called")
    # Provide the CSV filename to the function
    read_csv_and_store_in_database('Web Scraper/File Data/linkedin-jobs.csv')
    displayData = data.query.all()
    #print(f"Number of records: {len(displayData)}")
    return render_template('index.html', data = displayData)  # Replace with your template

if __name__ == '__main__':
    app.run(debug=True)

url = 'https://ca.linkedin.com/jobs/software-engineer-jobs?position=1&pageNum=0&currentJobId=3778290848'