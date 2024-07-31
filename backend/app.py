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


# The "register" route
@app.route('/survey/value-in-role', methods=['POST'])
@cross_origin(origin='http://localhost:5173/survey/value-in-role', supports_credentials=True)
def valueInRole():
    MAX_SIZE = 3  # The maximum size of the list
    option = request.json['option']

    print("The option the user picked is:", option)

    if len(option) > MAX_SIZE:
        option = option[:MAX_SIZE]
    
    for i in option:
        print(i)
    
    supabase.table('valueinrole').insert({'option1': option[0], 'option2': option[1], 'option3': option[2]}).execute()

    # user = supabase.table('users').insert({'username': username, 'email' : email, 'password': password}).execute()
    return jsonify({'message': 'Data successfully sent'}), 200


@app.route('/survey/roles-interested-in', methods=['POST'])
@cross_origin(origin='http://localhost:5173/survey/roles-interested-in', supports_credentials=True)
def rolesInterestedIn():
    MAX_SIZE = 5  # The maximum size of the list
    option = request.json['option']

    print("The option the user picked is:", option)

    if len(option) < MAX_SIZE:
        option += ["NULL"] * (MAX_SIZE - len(option))  # Fill with empty strings
    
    for i in option:
        print(i)
    
    supabase.table('rolesinterestedin').insert({'option1': option[0], 'option2': option[1], 'option3': option[2],  'option4': option[3],  'option5': option[4]}).execute()

    # user = supabase.table('users').insert({'username': username, 'email' : email, 'password': password}).execute()
    return jsonify({'message': 'Data successfully sent'}), 200

@app.route('/survey/like-to-work', methods=['POST'])
@cross_origin(origin='http://localhost:5173/survey/like-to-work', supports_credentials=True)
def likeToWork():
    MAX_SIZE = 2  # The maximum size of the list
    option = request.json['option']

    print("The option the user picked is:", option)

    if len(option) < MAX_SIZE:
        option += ["NULL"] * (MAX_SIZE - len(option))  # Fill with empty strings
    
    for i in option:
        print(i)
    
    supabase.table('liketowork').insert({'option1': option[0], 'option2': option[1]}).execute()

    # user = supabase.table('users').insert({'username': username, 'email' : email, 'password': password}).execute()
    return jsonify({'message': 'Data successfully sent'}), 200


@app.route('/survey/level-of-experience', methods=['POST'])
@cross_origin(origin='http://localhost:5173/survey/level-of-experience', supports_credentials=True)
def levelOfExperience():
    MAX_SIZE = 2  # The maximum size of the list
    option = request.json['option']

    print("The option the user picked is:", option)

    if len(option) < MAX_SIZE:
        option += ["NULL"] * (MAX_SIZE - len(option))  # Fill with empty strings
    
    for i in option:
        print(i)
    
    supabase.table('levelofexperience').insert({'option1': option[0], 'option2': option[1]}).execute()

    # user = supabase.table('users').insert({'username': username, 'email' : email, 'password': password}).execute()
    return jsonify({'message': 'Data successfully sent'}), 200


@app.route('/survey/company-size', methods=['POST'])
@cross_origin(origin='http://localhost:5173/survey/company-size', supports_credentials=True)
def companySize():
    MAX_SIZE = 1  # The maximum size of the list
    option = request.json['option']

    print("The option the user picked is:", option)

    if len(option) < MAX_SIZE:
        option += ["NULL"] * (MAX_SIZE - len(option))  # Fill with empty strings
    
    for i in option:
        print(i)
    
    supabase.table('companysize').insert({'option1': option[0]}).execute()

    # user = supabase.table('users').insert({'username': username, 'email' : email, 'password': password}).execute()
    return jsonify({'message': 'Data successfully sent'}), 200


@app.route('/survey/industries-excited-in', methods=['POST'])
@cross_origin(origin='http://localhost:5173/survey/industries-excited-in', supports_credentials=True)
def industriesExcitedIn():
    MAX_SIZE = 5  # The maximum size of the list
    option = request.json['option']

    print("The option the user picked is:", option)

    if len(option) < MAX_SIZE:
        option += ["NULL"] * (MAX_SIZE - len(option))  # Fill with empty strings
    
    for i in option:
        print(i)
    
    supabase.table('industriesexcitedin').insert({'option1': option[0], 'option2': option[1], 'option3': option[2], 'option4': option[3], 'option5': option[4]}).execute()

    # user = supabase.table('users').insert({'username': username, 'email' : email, 'password': password}).execute()
    return jsonify({'message': 'Data successfully sent'}), 200


@app.route('/survey/skills-enjoy-working-with', methods=['POST'])
@cross_origin(origin='http://localhost:5173/survey/skills-enjoy-working-with', supports_credentials=True)
def skillsEnjoyWorkingWith():
    MAX_SIZE = 15  # The maximum size of the list
    option = request.json['option']

    print("The option the user picked is:", option)

    if len(option) < MAX_SIZE:
        option += ["NULL"] * (MAX_SIZE - len(option))  # Fill with empty strings
    
    for i in option:
        print(i)
    
    supabase.table('skillsenjoyworkingwith').insert({'option1': option[0], 'option2': option[1], 'option3': option[2], 'option4': option[3], 'option5': option[4], 'option6': option[5], 'option7': option[6], 'option8': option[7], 'option9': option[8], 'option10': option[9], 'option11': option[10], 'option12': option[11], 'option13': option[12], 'option14': option[13], 'option15': option[14]}).execute()

    # user = supabase.table('users').insert({'username': username, 'email' : email, 'password': password}).execute()
    return jsonify({'message': 'Data successfully sent'}), 200


@app.route('/survey/minimum-expected-salary', methods=['POST'])
@cross_origin(origin='http://localhost:5173/survey/minimum-expected-salary', supports_credentials=True)
def minimumExpectedSalary():
    MAX_SIZE = 1  # The maximum size of the list
    option = request.json['option']

    print("The option the user picked is:", option)

    # if len(option) > MAX_SIZE:
    #     option = option[:MAX_SIZE]
    
    # for i in option:
    #     print(i)
    
    supabase.table('minimumexpectedsalary').insert({'option1': option}).execute()

    # user = supabase.table('users').insert({'username': username, 'email' : email, 'password': password}).execute()
    return jsonify({'message': 'Data successfully sent'}), 200


if __name__ == '__main__':
    app.run(debug=True)