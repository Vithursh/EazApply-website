# Import the linkedin_scraper function from your scraper module.
#from scraper import linkedin_scraper

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

def read_csv_and_store_in_database(csv_filename):
    with open(csv_filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row if it exists
        db.drop_all()
        with app.app_context():
            db.create_all()
            for row in csv_reader:
                # Assuming CSV columns match the model columns
                record = data(title=row[0], company=row[1], location=row[2], applyLink=row[3])
                db.session.add(record)
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