import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import re
import requests
import csv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pickle

from app import *

def increment_count():
    count = 0
    count+= 1
    print("'count' is:",count)
    return count

def getCookies():
    with open("linkedin_cookies.pkl", "wb") as file:
        pickle.dump(driver.get_cookies(), file)


def loadCookies():
    with open("linkedin_cookies.pkl", "rb") as file:
        cookies = pickle.load(file)

    for cookie in cookies:
        driver.add_cookie(cookie)


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
    linkdUsrname = "Vithuchayan@gmail.com"
    linkdPasswrd = "Chayan23"

    if increment_count() == 1:
        # Logging in
        username = driver.find_element(By.CSS_SELECTOR, ".text-color-text.font-sans.text-md.outline-0.bg-color-transparent.grow")
        username.send_keys(linkdUsrname + Keys.ENTER)

        password = driver.find_element(By.ID, "session_password")
        password.send_keys(linkdPasswrd + Keys.ENTER)
        getCookies()
    else:
        print("The 'loadCookies' function is being called")
        loadCookies()
    
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
    click_apply = driver.find_element(By.ID, id_name)
    click_apply.click()

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