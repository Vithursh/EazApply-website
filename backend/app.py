from flask import Flask, request, jsonify
from flask_cors import cross_origin
from supabase import create_client, Client
from dotenv import load_dotenv
import os, re
import requests

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


@app.route('/survey/value-in-role', methods=['POST'])
@cross_origin(origin='http://localhost:5173/survey/value-in-role', supports_credentials=True)
def valueInRole():
    data = request.get_json()
    options = data.get('option', [])
    
    # Pad the options list with None values if less than 3 options selected
    while len(options) < 3:
        options.append(None)
    
    try:
        supabase.table('valueinrole').insert({
            'option1': options[0],
            'option2': options[1],
            'option3': options[2]
        }).execute()
        
        return jsonify({"message": "Data successfully sent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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


def get_user_summary(text) -> list[str]:
    api_key = os.getenv("GEMINI_API_KEY")
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-1.5-flash:generateContent"
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


def convert_survey_answers_to_paragraph():
    
    try:
        # Get the first row from each table
        value_in_role = supabase.table('valueinrole').select('*').limit(1).execute()
        roles_interested = supabase.table('rolesinterestedin').select('*').limit(1).execute()
        like_to_work = supabase.table('liketowork').select('*').limit(1).execute()
        minimum_salary = supabase.table('minimumexpectedsalary').select('*').limit(1).execute()
        level_experience = supabase.table('levelofexperience').select('*').limit(1).execute()
        company_size = supabase.table('companysize').select('*').limit(1).execute()
        industries_excited = supabase.table('industriesexcitedin').select('*').limit(1).execute()
        skills_enjoy = supabase.table('skillsenjoyworkingwith').select('*').limit(1).execute()

        # Filter out None values and integers for all tables
        value_in_role_data = [value for item in value_in_role.data for value in item.values() if value is not None and not isinstance(value, int)]
        roles_interested_data = [value for item in roles_interested.data for value in item.values() if value is not None and not isinstance(value, int)]
        like_to_work_data = [value for item in like_to_work.data for value in item.values() if value is not None and not isinstance(value, int)]
        minimum_salary_data = [value for item in minimum_salary.data for value in item.values() if value is not None and not isinstance(value, int)]
        level_experience_data = [value for item in level_experience.data for value in item.values() if value is not None and not isinstance(value, int)]
        company_size_data = [value for item in company_size.data for value in item.values() if value is not None and not isinstance(value, int)]
        industries_excited_data = [value for item in industries_excited.data for value in item.values() if value is not None and not isinstance(value, int)]
        skills_enjoy_data = [value for item in skills_enjoy.data for value in item.values() if value is not None and not isinstance(value, int)]

        # Filter out NULL values for all tables
        value_in_role_data = [value for value in value_in_role_data if value != "NULL"]
        roles_interested_data = [value for value in roles_interested_data if value != "NULL"]
        like_to_work_data = [value for value in like_to_work_data if value != "NULL"]
        minimum_salary_data = [value for value in minimum_salary_data if value != "NULL"]
        level_experience_data = [value for value in level_experience_data if value != "NULL"]
        company_size_data = [value for value in company_size_data if value != "NULL"]
        industries_excited_data = [value for value in industries_excited_data if value != "NULL"]
        skills_enjoy_data = [value for value in skills_enjoy_data if value != "NULL"]

        # Print all data
        # print("Value in role:", value_in_role_data)
        # print("Roles interested in:", roles_interested_data)
        # print("Like to work:", like_to_work_data)
        # print("Minimum salary:", minimum_salary_data)
        # print("Level of experience:", level_experience_data)
        # print("Company size:", company_size_data)
        # print("Industries excited in:", industries_excited_data)
        # print("Skills enjoy working with:", skills_enjoy_data)

        # Create a comprehensive human-readable summary
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
        print(f"Error in getFirstRow: {str(e)}")
        return None


@app.route('/survey/minimum-expected-salary', methods=['POST'])
@cross_origin(origin='http://localhost:5173/survey/minimum-expected-salary', supports_credentials=True)
def minimumExpectedSalary():
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
    supabase.table('minimumexpectedsalary').insert({'option1': option_with_k}).execute()

    print("The text is: ", convert_survey_answers_to_paragraph())

    user_summary = get_user_summary(convert_survey_answers_to_paragraph())

    # Extract the first summary without brackets
    cleaned_summary = user_summary[0] if user_summary else ""  # Get first element of list

    print("The LLM came out with:", cleaned_summary)

    # Replace the insert line with this update operation
    # .match({'email': request.json.get('email')})\
    supabase.table('users')\
        .update({'summary': cleaned_summary})\
        .match({'email': "Someone123@gmail.com"})\
        .execute()

    return jsonify({'message': 'Data successfully sent'}), 200


if __name__ == '__main__':
    app.run(debug=True)