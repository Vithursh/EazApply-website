from flask import Flask, request, jsonify
from flask_cors import cross_origin
import sys
sys.path.append('/home/vithursh/Coding/EazApply/backend/Search Engine/WebCrawler/WebCrawler/spiders')
from clean import receiveJobData
from supabase import create_client, Client
from dotenv import load_dotenv
import os, re
import ctypes
import requests

app = Flask(__name__)
# CORS(app, origins='http://localhost:5173/register', supports_credentials=True)
load_dotenv()

# Initialize Supabase client variables
supabase_url = os.getenv('VITE_SUPABASE_URL')
supabase_key = os.getenv('VITE_SUPABASE_ANON_KEY')

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
    # response = supabase.table("users").select("email").execute()

    # print("Data:\n", response.data)

    # containSameEmail = False

    # for row in response.data:
    #     if email == row['email']:
    #         containSameEmail = True

    # # Email validation
    # regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(.[A-Z|a-z]{2,})+')

    # # Check for empty fields first
    # if username == "":
    #     print("Username is empty")
    #     return jsonify({'error': 'Username is empty'}), 201
    # elif password == "":
    #     print("Password is empty")
    #     return jsonify({'error': 'Password is empty'}), 201
    # elif email == "":
    #     print("Email is empty")
    #     return jsonify({'error': 'Email is empty'}), 201
    # elif containSameEmail == True:
    #     print("This email has already been registered with")
    #     return jsonify({'error': 'This email has already been registered with'}), 201
    # elif not re.fullmatch(regex, email):
    #     print("Email was not formatted correctly")
    #     return jsonify({'error': 'Email was not formatted correctly'}), 201
    
    # # If all checks pass, insert the new user into the 'user' table
    
    
    # # After a user signs up...
    # user = supabase.auth.sign_up({"email": email, "password": password})
    
    # # Insert a new row into the 'users' table
    # supabase.table('users').insert({'user_id': user.data.id, 'username': username}).execute()

    # # user = supabase.table('users').insert({'username': username, 'email' : email, 'password': password}).execute()
    # return jsonify({'message': 'User created successfully'}), 200

    # first check if email exists
    # this could be using supabase.auth.admin.get_user_by_email
    user = supabase.auth.admin.get_user_by_email(email)
    if user is not None:
        # email already used
        return {"success": False, "error": "Email already in use"}, 409
    
    # else proceed to sign up
    result = supabase.auth.sign_up({ "email": email, "password": password })
    if result.error:
        # handle error
        return {"success": False, "error": result.error.message}, 400
    else:
        # success
        # maybe also insert username into a “profiles” table or whatever
        return {"success": True, "data": result.user}, 201


@app.route('/dashboard', methods=['GET'])
@cross_origin(origin='http://localhost:5173/dashboard', supports_credentials=True)
def dashBoard():
    # Get only the userId
    user_id = request.args.get('userId')
    # print(f"Received userId: {user_id} in the backend dashboard route")
    # Call the loadData function with the userId and return the data as JSON
    # Define the path to the shared library
    lib_path = os.path.join(os.path.dirname(__file__), '/home/vithursh/Coding/EazApply/backend/Search Engine/FilterSystem/libfilterSystem.so')

    # Load the shared library
    shared_library = ctypes.CDLL(lib_path)

    # Define the argument and return types
    shared_library.loadDatabaseData.argtypes = [ctypes.c_char_p]
    shared_library.loadDatabaseData.restype = ctypes.c_void_p

    # Convert the string to bytes
    user_id_bytes = user_id.encode('utf-8')

    # Call the function
    result = shared_library.loadDatabaseData(user_id_bytes)
    return jsonify(receiveJobData()), 200


@app.route('/survey/value-in-role/<uuid>', methods=['POST'])
@cross_origin(origin='http://localhost:5173', supports_credentials=True)
def valueInRole(uuid):
    print(f"In the backend the user is: {uuid}")
    data = request.get_json()
    options = data.get('option', [])
    
    # Pad the options list with None values if less than 3 options selected
    while len(options) < 3:
        options.append(None)
    
    try:
        supabase.table('valueinrole').insert({
            'user_id': uuid,
            'option1': options[0],
            'option2': options[1],
            'option3': options[2]
        }).execute()
        
        return jsonify({"message": "Data successfully sent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/survey/roles-interested-in/<uuid>', methods=['POST'])
@cross_origin(origin='http://localhost:5173', supports_credentials=True)
def rolesInterestedIn(uuid):
    print(f"In the backend the user is: {uuid}")
    MAX_SIZE = 5  # The maximum size of the list
    option = request.json['option']

    print("The option the user picked is:", option)

    if len(option) < MAX_SIZE:
        option += ["NULL"] * (MAX_SIZE - len(option))  # Fill with empty strings
    
    for i in option:
        print(i)
    
    supabase.table('rolesinterestedin').insert({'user_id': uuid, 'option1': option[0], 'option2': option[1], 'option3': option[2],  'option4': option[3],  'option5': option[4]}).execute()

    # user = supabase.table('users').insert({'username': username, 'email' : email, 'password': password}).execute()
    return jsonify({'message': 'Data successfully sent'}), 200

@app.route('/survey/like-to-work/<uuid>', methods=['POST'])
@cross_origin(origin='http://localhost:5173', supports_credentials=True)
def likeToWork(uuid):
    print(f"In the backend the user is: {uuid}")
    MAX_SIZE = 2  # The maximum size of the list
    option = request.json['option']

    print("The option the user picked is:", option)

    if len(option) < MAX_SIZE:
        option += ["NULL"] * (MAX_SIZE - len(option))  # Fill with empty strings
    
    for i in option:
        print(i)
    
    supabase.table('liketowork').insert({'user_id': uuid, 'option1': option[0], 'option2': option[1]}).execute()

    # user = supabase.table('users').insert({'username': username, 'email' : email, 'password': password}).execute()
    return jsonify({'message': 'Data successfully sent'}), 200


@app.route('/survey/level-of-experience/<uuid>', methods=['POST'])
@cross_origin(origin='http://localhost:5173', supports_credentials=True)
def levelOfExperience(uuid):
    print(f"In the backend the user is: {uuid}")
    MAX_SIZE = 2  # The maximum size of the list
    option = request.json['option']

    print("The option the user picked is:", option)

    if len(option) < MAX_SIZE:
        option += ["NULL"] * (MAX_SIZE - len(option))  # Fill with empty strings
    
    for i in option:
        print(i)
    
    supabase.table('levelofexperience').insert({'user_id': uuid, 'option1': option[0], 'option2': option[1]}).execute()

    # user = supabase.table('users').insert({'username': username, 'email' : email, 'password': password}).execute()
    return jsonify({'message': 'Data successfully sent'}), 200


@app.route('/survey/company-size/<uuid>', methods=['POST'])
@cross_origin(origin='http://localhost:5173', supports_credentials=True)
def companySize(uuid):
    print(f"In the backend the user is: {uuid}")
    MAX_SIZE = 1  # The maximum size of the list
    option = request.json['option']

    print("The option the user picked is:", option)

    if len(option) < MAX_SIZE:
        option += ["NULL"] * (MAX_SIZE - len(option))  # Fill with empty strings
    
    for i in option:
        print(i)
    
    supabase.table('companysize').insert({'user_id': uuid, 'option1': option[0]}).execute()

    # user = supabase.table('users').insert({'username': username, 'email' : email, 'password': password}).execute()
    return jsonify({'message': 'Data successfully sent'}), 200


@app.route('/survey/industries-excited-in/<uuid>', methods=['POST'])
@cross_origin(origin='http://localhost:5173', supports_credentials=True)
def industriesExcitedIn(uuid):
    print(f"In the backend the user is: {uuid}")
    MAX_SIZE = 5  # The maximum size of the list
    option = request.json['option']

    print("The option the user picked is:", option)

    if len(option) < MAX_SIZE:
        option += ["NULL"] * (MAX_SIZE - len(option))  # Fill with empty strings
    
    for i in option:
        print(i)
    
    supabase.table('industriesexcitedin').insert({'user_id': uuid, 'option1': option[0], 'option2': option[1], 'option3': option[2], 'option4': option[3], 'option5': option[4]}).execute()

    # user = supabase.table('users').insert({'username': username, 'email' : email, 'password': password}).execute()
    return jsonify({'message': 'Data successfully sent'}), 200


@app.route('/survey/skills-enjoy-working-with/<uuid>', methods=['POST'])
@cross_origin(origin='http://localhost:5173', supports_credentials=True)
def skillsEnjoyWorkingWith(uuid):
    print(f"In the backend the user is: {uuid}")
    MAX_SIZE = 15  # The maximum size of the list
    option = request.json['option']

    print("The option the user picked is:", option)

    if len(option) < MAX_SIZE:
        option += ["NULL"] * (MAX_SIZE - len(option))  # Fill with empty strings
    
    for i in option:
        print(i)
    
    supabase.table('skillsenjoyworkingwith').insert({'user_id': uuid, 'option1': option[0], 'option2': option[1], 'option3': option[2], 'option4': option[3], 'option5': option[4], 'option6': option[5], 'option7': option[6], 'option8': option[7], 'option9': option[8], 'option10': option[9], 'option11': option[10], 'option12': option[11], 'option13': option[12], 'option14': option[13], 'option15': option[14]}).execute()

    # user = supabase.table('users').insert({'username': username, 'email' : email, 'password': password}).execute()
    return jsonify({'message': 'Data successfully sent'}), 200


def get_user_summary(text) -> list[str]:
    api_key = os.getenv("GEMINI_API_KEY")
    # Using gemini-2.5-flash
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.5-flash:generateContent"
        f"?key={api_key}"
    )

    instruction = (
        "You are a web‐page summarization assistant, but now summarize a candidate’s preferences.\n"
        "1) Remove any extraneous labels or bullet syntax.\n"
        "2) Merge any fragments into full sentences.\n"
        "3) Summarize all the profile details into a single cohesive paragraph "
        "that covers these fields: experience level, role type, location, company size, "
        "salary expectation, values, industries, and key skills.\n"
        "4) Return **only** that one paragraph in plain English. No JSON, no lists, no extra commentary—just the summary."
    )

    payload = {
        "contents": [
            {"parts": [{"text": instruction}, {"text": text}]}
        ],
        "generationConfig": {
            "maxOutputTokens": 2048,
            "temperature": 0.0
        }
    }

    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    # Extract the raw text response
    body = resp.json()
    raw = body["candidates"][0]["content"]["parts"][0]["text"]
    
    # Split on double newlines into paragraphs
    paragraphs = [p.strip() for p in raw.split("\n\n") if p.strip()]
    return paragraphs


def convert_survey_answers_to_paragraph(userID):
    try:
        # Fetch data filtered by the specific userID
        value_in_role = supabase.table('valueinrole').select('*').eq('user_id', userID).execute()
        roles_interested = supabase.table('rolesinterestedin').select('*').eq('user_id', userID).execute()
        like_to_work = supabase.table('liketowork').select('*').eq('user_id', userID).execute()
        minimum_salary = supabase.table('minimumexpectedsalary').select('*').eq('user_id', userID).execute()
        level_experience = supabase.table('levelofexperience').select('*').eq('user_id', userID).execute()
        company_size = supabase.table('companysize').select('*').eq('user_id', userID).execute()
        industries_excited = supabase.table('industriesexcitedin').select('*').eq('user_id', userID).execute()
        skills_enjoy = supabase.table('skillsenjoyworkingwith').select('*').eq('user_id', userID).execute()

        # Helper to clean data: removes Nones, integers (like the ID itself), and "NULL" strings
        def clean_data(response):
            return [
                value for item in response.data 
                for value in item.values() 
                if value is not None and not isinstance(value, int) and value != "NULL"
            ]

        # Apply cleaning
        value_in_role_data = clean_data(value_in_role)
        roles_interested_data = clean_data(roles_interested)
        like_to_work_data = clean_data(like_to_work)
        minimum_salary_data = clean_data(minimum_salary)
        level_experience_data = clean_data(level_experience)
        company_size_data = clean_data(company_size)
        industries_excited_data = clean_data(industries_excited)
        skills_enjoy_data = clean_data(skills_enjoy)

        # Create summary
        text = f"""
                Profile Summary:
                - Values in role: {', '.join(value_in_role_data)}
                - Interested in roles: {', '.join(roles_interested_data)}
                - Preferred locations: {', '.join(like_to_work_data)}
                - Minimum expected salary: ${', '.join(minimum_salary_data)} per year
                - Level of experience: {', '.join(level_experience_data)}
                - Preferred company size: {', '.join(company_size_data)}
                - Industries interested in: {', '.join(industries_excited_data)}
                - Skills: {', '.join(skills_enjoy_data)}
                """
        
        return text
        
    except Exception as e:
        print(f"Error in convert_survey_answers_to_paragraph: {str(e)}")
        return None


@app.route('/survey/minimum-expected-salary/<uuid>', methods=['POST'])
@cross_origin(origin='http://localhost:5173', supports_credentials=True)
def minimumExpectedSalary(uuid):
    print(f"In the backend the user is: {uuid}")
    MAX_SIZE = 1  # The maximum size of the list
    option = request.json['option']

    print("The option the user picked is:", option)

    # Add 'k' to the string value
    option_with_k = str(option) + 'K'

    # if len(option) > MAX_SIZE:
    #     option = option[:MAX_SIZE]
    
    # for i in option:
    #     print(i)
    
    # Insert the data into the database
    supabase.table('minimumexpectedsalary').insert({'user_id': uuid, 'option1': option_with_k}).execute()

    print("The text is: ", convert_survey_answers_to_paragraph(uuid))

    user_summary = get_user_summary(convert_survey_answers_to_paragraph(uuid))

    # Extract the first summary without brackets
    cleaned_summary = user_summary[0] if user_summary else ""  # Get first element of list

    print("The LLM came out with:", cleaned_summary)

    # Insert the users profile into the database
    supabase.table('users') \
    .insert({
        'user_id': uuid,         # Include the identifier in the insert object
        'summary': cleaned_summary
    }) \
    .execute()

    return jsonify({'message': 'Data successfully sent'}), 200


if __name__ == '__main__':
    app.run(debug=True)