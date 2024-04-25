import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import random

import re
import requests
import csv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pickle
import os

from app import *

count = 0
global x

def increment_count():
    global count
    count+= 1
    print("'count' is:",count)
    return count


def is_file_found(file_path):
    print("The path to the directory is:",os.path.isfile(file_path))
    return os.path.isfile(file_path)


def savecookies():
    print("saving cookie")
    time.sleep(10)
    cookies = driver.get_cookies()
    for cookie in cookies:
        if(cookie['name']=='li_at'):
            cookie['domain']='.linkedin.com'
            x={
            'name': 'li_at',
            'value': cookie['value'],
            'domain': '.linkedin.com'
            }
            break
    pickle.dump(x , open("cookies.pkl","wb"))
    print('cookies saved')


def loadcookie():
    print("loading cookie")
    cookies = pickle.load(open("cookies.pkl", "rb"))
    print(cookies)
    driver.add_cookie(cookies)
    print('loaded cookie')


def logInLinkedin(string):
    print(increment_count())
    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.linkedin.com/")
    print("Logged into linkedin")

    # linkedin credentials
    #linkdUsrname = "Vithursh0512@gmail.com"
    #linkdPasswrd = "VithurshEngineerBoss"

    # linkedin credentials
    #linkdUsrname = "Vithuchayan@gmail.com"
    #linkdPasswrd = "Chayan23"

    # Burner account
    global linkdUsrname
    linkdUsrname = "daniel.garcia2001211@gmail.com"
    global linkdPasswrd
    linkdPasswrd = "Chayan23"

    if not is_file_found("cookies.pkl"):
        # Logging in
        print("getting the cookie")
        username = driver.find_element(By.CSS_SELECTOR, ".text-color-text.font-sans.text-md.outline-0.bg-color-transparent.grow")
        username.send_keys(linkdUsrname + Keys.ENTER)

        password = driver.find_element(By.ID, "session_password")
        password.send_keys(linkdPasswrd + Keys.ENTER)
        savecookies()
    else:
        print("The 'loadCookies' function is being called")
        loadcookie()
        #driver.refresh()
    
    jobPost(string)


def jobPost(c_string):
    print("\nFetching link...\n")
    time.sleep(5)
    driver.get(c_string)

    # Wait 20 seconds
    # print("Waiting 20 seconds to make sure page loads\n")
    # driver.implicitly_wait(20)
    
    # Use ID selector
    # id_name = "ember82"
    class_name = "jobs-apply-button--top-card"

    # Wait until the element is visible
    # WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, id_name)))

    # Find the element and click it
    try:
        click_apply = driver.find_element(By.CLASS_NAME, class_name)
        click_apply.click()
        print("Element found, proceeding to next step...\n")

        # Assuming driver.window_handles[0] is the first tab and driver.window_handles[1] is the new tab
        driver.switch_to.window(driver.window_handles[0])  # Switch to new tab
        driver.close()  # Close the first tab
        driver.switch_to.window(driver.window_handles[0])  # Switch back to what is now the only tab
        time.sleep(10)
        print("Sleeping for 60 seconds...")
        time.sleep(15)
    except NoSuchElementException:
        print("Element not found, moving on...\n")
        print("Sleeping for 60 seconds...")
        time.sleep(15)

    # Get the URL the bot is at
    global current_url
    current_url = driver.current_url
    if check_if_Contains_Work_day(current_url):
        # Exacute function for filling out the form
        print("Link contains '.myworkdayjobs.com' in it\n")
        fillOutApplication(current_url)
    else:
        print("Link does not contain '.myworkdayjobs.com' in it")


def check_if_Contains_Work_day(url):
    print("The current URL is:", url)
    if ".myworkdayjobs.com" in url:
        return True
    else:
        return False


def fillOutApplication(url):
    print("You have reached the 'fillOutApplication' function\n")

    class_name_workday = "css-b3pn3b"

    # Find the element and click it
    try:
        click_apply_workday = driver.find_element(By.CLASS_NAME, class_name_workday)
        click_apply_workday.click()
        print("Workday 'Apply' element found, proceeding to next step...\n")
    except NoSuchElementException:
        print("Workday 'Apply' element not found, moving on...\n")

    # Clicks the manually apply button
    class_name_manually = "css-1s1r74k"

    # Find the element and click it
    try:
        click_apply_manually = driver.find_element(By.CLASS_NAME, class_name_manually)
        click_apply_manually.click()
        print("'Apply Manually' element found, proceeding to next step...\n")

        # Open CSV file that stores the companies that are 
        file_path = "Web Scraper/File Data/Added-workday-companies.csv"

        # Split the URL into parts based on "/"
        parts = current_url.split("/")

        # Get the part after the 6th "/" (which is at index 5 because indexing starts at 0)
        part = parts[2]

        # Split this part based on "-"
        sub_parts = part.split(".")

        # Get the part before "_JR" (which is the first part of sub_parts)
        text = sub_parts[0]

        print("The text that is going to be stored in the file is:",text,"\n\n")

        # Checks to see if the user needs to login or create an account

        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Create a CSV reader
            reader = csv.reader(file)

            # Check if the text exists in the file
            text_exists = any(text in row for row in reader)

        # If the text doesn't exist, append it to the file
        if not text_exists:
            with open(file_path, 'a', newline='') as file:
                writer = csv.writer(file)
                # Write the text to the file
                writer.writerow([text])
                print("Storing company name in CSV file\n")
            create_account()
        else:
            print("Call the log into account function\n")

    except NoSuchElementException:
        print("'Apply Manually' element not found, moving on...\n")
    

def create_account():
    # Clicks the Create Account button
    class_name_create_account = "css-14pfav7"
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name_create_account)))

    # Find the element and click it
    try:
        click_apply_create_account = driver.find_element(By.CLASS_NAME, class_name_create_account)
        click_apply_create_account.click()
        print("'Create Account' element found, proceeding to next step...\n")
    except NoSuchElementException:
        print("'Create Account' element not found, moving on...\n")


    # Clicks the Create Account button
    class_name_email = "input-6"

    global click_apply_email

    # Find the element and click it
    try:
        click_apply_email = driver.find_element(By.ID, class_name_email)
        click_apply_email.click()
        click_apply_email.send_keys(linkdUsrname + Keys.TAB)
        print("'Email' element found, proceeding to next step...\n")
        time.sleep(15)
    except NoSuchElementException:
        print("'Email' element not found, moving on...\n")


    linkdPasswrd = "Chayan@23"
    # Clicks the Create Account button
    class_name_password = "input-7"
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, class_name_password)))

    # Find the element and click it
    try:
        click_apply_password = driver.find_element(By.ID, class_name_password)
        click_apply_password.click()
        print(linkdPasswrd)
        time.sleep(10)
        click_apply_password.send_keys(linkdPasswrd + Keys.TAB)
        print("'Password' element found, proceeding to next step...\n")
    except NoSuchElementException:
        print("'Password' element not found, moving on...\n")

    
    class_name_verify_password = "input-8"
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, class_name_verify_password)))

    # Find the element and click it
    try:
        click_apply_verify_password = driver.find_element(By.ID, class_name_verify_password)
        click_apply_verify_password.click()
        click_apply_verify_password.send_keys(linkdPasswrd)
        print("'Verify Password' element found, proceeding to next step...\n")
    except NoSuchElementException:
        print("'Verify Password' element not found, moving on...\n")


    class_name_verify_checkBox = "css-d3pjdr"
    #WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name_verify_checkBox)))

    # Find the element and click it
    try:
        click_apply_checkBox = driver.find_element(By.CLASS_NAME, class_name_verify_checkBox)
        click_apply_checkBox.click()
        print("'Check Box' element found, proceeding to next step...\n")
    except NoSuchElementException:
        print("'Check Box' element not found, moving on...\n")
    
    time.sleep(10)


    class_name_create_account_button = "css-1s1r74k"
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name_create_account_button)))

    # Find the element and click it
    try:
        click_apply_create_account_button = driver.find_element(By.CLASS_NAME, class_name_create_account_button)
        click_apply_create_account_button.click()
        print("'Create Account button' element found, proceeding to next step...\n")
    except NoSuchElementException:
        print("'Create Account button' element not found, moving on...\n")