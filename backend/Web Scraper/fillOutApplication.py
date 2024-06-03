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

import linkedin_bot as link_bot

def my_Information_page(current_workday_url):
    driver = link_bot.setup_driver()
    driver.get(current_workday_url)
    link_bot.log_into_account()
    # id_name_referralSource = "input-1"
    # WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, id_name_referralSource)))

    # # Find the element and click it
    # try:
    #     click_apply_referralSource = driver.find_element(By.ID, id_name_referralSource)
    #     click_apply_referralSource.click()
    #     click_apply_referralSource.send_keys("Other" + Keys.ENTER + Keys.ENTER)
    #     print("'ReferralSource button' element found, proceeding to next step...\n")
    # except NoSuchElementException:
    #     print("'referralSource button' element not found, moving on...\n")


    id_name_country = "input-2"
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, id_name_country)))

    # Find the element and click it
    try:
        click_apply_country = driver.find_element(By.ID, id_name_country)
        click_apply_country.click()
        click_apply_country.send_keys("Canada" + Keys.ENTER)
        print("'Country button' element found, proceeding to next step...\n")
    except NoSuchElementException:
        print("'Country button' element not found, moving on...\n")


    id_name_first_name = "input-3"
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, id_name_first_name)))

    # Find the element and click it
    try:
        click_apply_first_name = driver.find_element(By.ID, id_name_first_name)
        click_apply_first_name.click()
        click_apply_first_name.send_keys("Vithursh")
        print("'First Name' element found, proceeding to next step...\n")
    except NoSuchElementException:
        print("'First Name' element not found, moving on...\n")

    
    id_name_last_name = "input-4"
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, id_name_last_name)))

    # Find the element and click it
    try:
        click_apply_last_name = driver.find_element(By.ID, id_name_last_name)
        click_apply_last_name.click()
        click_apply_last_name.send_keys("Chayan")
        print("'Last Name' element found, proceeding to next step...\n")
    except NoSuchElementException:
        print("'Last Name' element not found, moving on...\n")


    id_name_address = "input-6"
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, id_name_address)))

    # Find the element and click it
    try:
        click_apply_address = driver.find_element(By.ID, id_name_address)
        click_apply_address.click()
        click_apply_address.send_keys("Address")
        print("'Address' element found, proceeding to next step...\n")
    except NoSuchElementException:
        print("'Address' element not found, moving on...\n")

    
    id_name_city = "input-8"
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, id_name_city)))

    # Find the element and click it
    try:
        click_apply_city = driver.find_element(By.ID, id_name_city)
        click_apply_city.click()
        click_apply_city.send_keys("Markham")
        print("'City' element found, proceeding to next step...\n")
    except NoSuchElementException:
        print("'City' element not found, moving on...\n")


    id_name_province = "input-9"
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, id_name_province)))

    # Find the element and click it
    try:
        click_apply_province = driver.find_element(By.ID, id_name_province)
        click_apply_province.click()
        click_apply_province.send_keys("Quebec" + Keys.ENTER)
        print("'Province' element found, proceeding to next step...\n")
    except NoSuchElementException:
        print("'Province' element not found, moving on...\n")


    id_name_postal_code = "input-10"
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, id_name_postal_code)))

    # Find the element and click it
    try:
        click_apply_postal_code = driver.find_element(By.ID, id_name_postal_code)
        click_apply_postal_code.click()
        click_apply_postal_code.send_keys("k7g 7f9")
        print("'Postal Code' element found, proceeding to next step...\n")
    except NoSuchElementException:
        print("'Postal Code' element not found, moving on...\n")


    id_name_phone = "input-12"
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, id_name_phone)))

    # Find the element and click it
    try:
        click_apply_phone = driver.find_element(By.ID, id_name_phone)
        click_apply_phone.click()
        click_apply_phone.send_keys("Mobile")
        print("'Phone' element found, proceeding to next step...\n")
    except NoSuchElementException:
        print("'Phone' element not found, moving on...\n")