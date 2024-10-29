from scrapy.crawler import CrawlerProcess
from EazApplybot import EazApplySpider
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import shutil
import re
import ctypes
import requests
import numpy as np

# Load environment variables from .env file
load_dotenv()

# Access the variables
supabase_url = os.getenv("REACT_APP_SUPABASE_URL")
supabase_key = os.getenv("REACT_APP_SUPABASE_KEY")

def run_spider():
    process = CrawlerProcess(settings={
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 5,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
        'AUTOTHROTTLE_DEBUG': False,
    })
    process.crawl(EazApplySpider, capacity=5, refill_time=5, refill_amount=1)
    process.start()

if __name__ == '__main__':
    run_spider()

# Initialize Supabase client
supabase: Client = create_client(supabase_url, supabase_key)

def flatten_data(data_list, fields):
    # Extract the specified fields from each dictionary and flatten the list
    flattened_data = [item[field] for item in data_list for field in fields]
    
    # Convert to a NumPy array if desired
    return np.array(flattened_data)


def add_attributes(table_name):
    response = supabase.table(table_name).select("*").execute()
    # Specify the fields you want to extract
    fields_to_extract = ['id']
    count = 0
    if response.data:
        # Check the number of attributes in each dictionary
        for index, item in enumerate(response.data):
            num_attributes = len(item)
            for data in range(1, num_attributes):
                count+=1
                fields_to_extract.append(f'option{count}')
    else:
        print("Error fetching data")
    
    # Call the function
    flattened_array = flatten_data(response.data, fields_to_extract)
    print("The data: ", flattened_array)
    print(f"The structre contains {count} numbers of attribute place holders for the {table_name} table.")

    return flattened_array


# Load the shared library
lib = ctypes.CDLL('/home/vithursh/Coding/EazApply/backend/Search Engine/FilterSystem/libfilterSystem.so')

# Define the argument types for receiveData (array of C-style strings and an integer)
lib.receiveData.argtypes = (
    ctypes.POINTER(ctypes.c_char_p), ctypes.c_int,  # companysize
    ctypes.POINTER(ctypes.c_char_p), ctypes.c_int,  # industriesexcitedin
    ctypes.POINTER(ctypes.c_char_p), ctypes.c_int,  # levelofexperience
    ctypes.POINTER(ctypes.c_char_p), ctypes.c_int,  # liketowork
    ctypes.POINTER(ctypes.c_char_p), ctypes.c_int,  # minimumexpectedsalary
    ctypes.POINTER(ctypes.c_char_p), ctypes.c_int,  # rolesinterestedin
    ctypes.POINTER(ctypes.c_char_p), ctypes.c_int,  # skillsenjoyworkingwith
    ctypes.POINTER(ctypes.c_char_p), ctypes.c_int   # valueinrole
)

# Convert Python strings to C-style strings (ctypes array of `c_char_p`)
c_companysize_array = (ctypes.c_char_p * len(add_attributes("companysize")))(*[str(element).encode('utf-8') for element in add_attributes("companysize")])

# Convert Python strings to C-style strings (ctypes array of `c_char_p`)
c_industriesexcitedin_array = (ctypes.c_char_p * len(add_attributes("industriesexcitedin")))(*[str(element).encode('utf-8') for element in add_attributes("industriesexcitedin")])

# Convert Python strings to C-style strings (ctypes array of `c_char_p`)
c_levelofexperience_array = (ctypes.c_char_p * len(add_attributes("levelofexperience")))(*[str(element).encode('utf-8') for element in add_attributes("levelofexperience")])

# Convert Python strings to C-style strings (ctypes array of `c_char_p`)
c_liketowork_array = (ctypes.c_char_p * len(add_attributes("liketowork")))(*[str(element).encode('utf-8') for element in add_attributes("liketowork")])

# Convert Python strings to C-style strings (ctypes array of `c_char_p`)
c_minimumexpectedsalary_array = (ctypes.c_char_p * len(add_attributes("minimumexpectedsalary")))(*[str(element).encode('utf-8') for element in add_attributes("minimumexpectedsalary")])

# Convert Python strings to C-style strings (ctypes array of `c_char_p`)
c_rolesinterestedin_array = (ctypes.c_char_p * len(add_attributes("rolesinterestedin")))(*[str(element).encode('utf-8') for element in add_attributes("rolesinterestedin")])

# Convert Python strings to C-style strings (ctypes array of `c_char_p`)
c_skillsenjoyworkingwith_array = (ctypes.c_char_p * len(add_attributes("skillsenjoyworkingwith")))(*[str(element).encode('utf-8') for element in add_attributes("skillsenjoyworkingwith")])

# Convert Python strings to C-style strings (ctypes array of `c_char_p`)
c_valueinrole_array = (ctypes.c_char_p * len(add_attributes("valueinrole")))(*[str(element).encode('utf-8') for element in add_attributes("valueinrole")])

# Call the C++ function with the arrays and its lengths
lib.receiveData(c_companysize_array, len(add_attributes("companysize")), 
                c_industriesexcitedin_array, len(add_attributes("industriesexcitedin")), 
                c_levelofexperience_array, len(add_attributes("levelofexperience")), 
                c_liketowork_array, len(add_attributes("liketowork")), 
                c_minimumexpectedsalary_array, len(add_attributes("minimumexpectedsalary")), 
                c_rolesinterestedin_array, len(add_attributes("rolesinterestedin")), 
                c_skillsenjoyworkingwith_array, len(add_attributes("skillsenjoyworkingwith")), 
                c_valueinrole_array, len(add_attributes("valueinrole")))