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

    # Burner account
    linkdUsrname = "daniel.garcia2001211@gmail.com"
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
    print("\nFetching link\n")
    time.sleep(5)
    driver.get(c_string)

    # Use ID selector
    id_name = "ember82"

    # Wait until the element is visible
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, id_name)))

    # Find the element and click it
    #try:
    click_apply = driver.find_element(By.ID, id_name)
       #if id_name != "ember82":
           # print("Link does not contain 'Apply' button")
       # else:
    click_apply.click()
            #print("Link does contain 'Apply' button")
    #except NoSuchElementException:
       # print("Element not found, moving on...")
    #except TimeoutException:
        #print("Operation timed out, moving on...")

    print("Sleeping for 60 seconds...")
    time.sleep(60)

    # Get the URL the bot is at 
    current_url = driver.current_url
    if check_if_Contains_Work_day(current_url):
        # Exacute function for filling out the form
        fillOutApplication(current_url)
    else:
        print("Link does not contain '.wd5.myworkdayjobs.com' in it")


def check_if_Contains_Work_day(url):
    if ".wd5.myworkdayjobs.com" in url:
        return True
    else:
        return False


def fillOutApplication(url):
    print("You have reached the 'fillOutApplication' function")