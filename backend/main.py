from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from supabase import create_client, Client
from dotenv import load_dotenv
import os, re

app = Flask(__name__)
# CORS(app, origins='http://localhost:5173/register', supports_credentials=True)
load_dotenv()

# Initialize Supabase client variables
supabase_url = os.getenv('REACT_APP_SUPABASE_URL')
supabase_key = os.getenv('REACT_APP_SUPABASE_KEY')

# Initialize Supabase client
url: str = supabase_url
key: str = supabase_key
supabase: Client = create_client(url, key)

@app.route('/')
def home():
    # Use the Supabase client for database operations
    # For example, to fetch all rows from a table:
    # result = supabase.table('your-table-name').select('*')
    return 'Backend running!'

# The "register" route
@app.route('/register', methods=['POST'])
@cross_origin(origin='http://localhost:5173/register', supports_credentials=True)
def register():
    # data = request.json
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    # Select all rows from a table and get a specific attribute
    response = supabase.table("users").select("email").execute()

    # print("Data:\n", response.data)

    containSameEmail = False

    for row in response.data:
        if email == row['email']:
            containSameEmail = True

    # Email validation
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(.[A-Z|a-z]{2,})+')

    # Check for empty fields first
    if username == "":
        print("Username is empty")
        return jsonify({'error': 'Username is empty'}), 201
    elif password == "":
        print("Password is empty")
        return jsonify({'error': 'Password is empty'}), 201
    elif email == "":
        print("Email is empty")
        return jsonify({'error': 'Email is empty'}), 201
    elif containSameEmail == True:
        print("This email has already been registered with")
        return jsonify({'error': 'This email has already been registered with'}), 201
    elif not re.fullmatch(regex, email):
        print("Email was not formatted correctly")
        return jsonify({'error': 'Email was not formatted correctly'}), 201
    
    # If all checks pass, insert the new user into the 'user' table
    
    
    # After a user signs up...
    user = supabase.auth.sign_up({"email": email, "password": password})
    
    # Insert a new row into the 'users' table
    supabase.table('users').insert({'user_id': user.data.id, 'username': username}).execute()

    # user = supabase.table('users').insert({'username': username, 'email' : email, 'password': password}).execute()
    return jsonify({'message': 'User created successfully'}), 200

    # Create a new user
    #user = supabase.auth.sign_up(username, password)

if __name__ == '__main__':
    app.run(debug=True)