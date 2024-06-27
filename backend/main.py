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

    # Email validation
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(.[A-Z|a-z]{2,})+')

    if re.fullmatch(regex, email):
        if username == "":
            print("username is empty")
            return jsonify({'error': 'Username is empty'}), 400
        elif password == "":
            print("password is empty")
            return jsonify({'error': 'Password is empty'}), 400
        else:
            # Insert the new user into the 'user' table
            user = supabase.table('users').insert({'username': username, 'email' : email, 'password': password}).execute()
            return jsonify({'message': 'User created successfully'}), 200
    elif email == "":
        print("Email is empty")
        return jsonify({'error': 'Email is empty'}), 400
    else:
        print("Email was not formatted correctly")
        return jsonify({'error': 'Email was not formatted correctly'}), 400

    # Create a new user
    #user = supabase.auth.sign_up(username, password)

    
    # if user.status_code == 201:
        # return jsonify({'message': 'User created successfully'}), 200
    # else:
        # return jsonify({'error': 'Registration failed'}), 400

if __name__ == '__main__':
    app.run(debug=True)