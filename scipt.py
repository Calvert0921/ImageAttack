# -*- coding: utf-8 -*-
__author__ = 'DELL'
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

def login():
    chrome_driver_path = r"D:\chromedriver\chromedriver.exe"

    user_email = "calvert0921@outlook.com"
    password = "fangzhizhou123"
    os.system('taskkill /im chromedriver.exe /F') # Make sure all processes closed
    os.system('taskkill /im chrome.exe /F') # Make sure all processes closed
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options,driver_executable_path=chrome_driver_path)
    driver.get('https://chat.openai.com/?model=gpt-4')
    time.sleep(1) 
    try:
        # Click login button
        login_button = driver.find_element(By.XPATH,'//div[contains(@class,"mt-5")]/div/button[1]')
        time.sleep(1) 
        login_button.click()
        time.sleep(3) 

        # Enter user email
        user_email_input = driver.find_element(By.XPATH,'/html/body/div/main/section/div/div/div/div[1]/div/form/div[1]/div/div/div/input')
        user_email_input.click() 
        user_email_input.clear()
        user_email_input.send_keys(user_email)
        time.sleep(1) 

        # Click Next button
        login_next_step_button = driver.find_element(By.XPATH,'/html/body/div/main/section/div/div/div/div[1]/div/form/div[2]/button')
        login_next_step_button.click()
        time.sleep(1)

        # Enter password
        user_password_input = driver.find_element(By.XPATH,'/html/body/div/main/section/div/div/div/form/div[1]/div/div[2]/div/input')
        user_password_input.click() 
        user_password_input.clear()
        user_password_input.send_keys(password)
        time.sleep(1) 

        # Submit
        submit_button = driver.find_element(By.XPATH,'/html/body/div/main/section/div/div/div/form/div[2]/button')
        submit_button.click()
        time.sleep(1)
    except Exception as e:
        print("here are some errors happened:",e)
    return driver 

def upload_image(driver):
    upload_button = driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/form/div/div/div/div/div/input')
    upload_button.send_keys("./dataset/test_files/200.png")
    
    time.sleep(10000)
    # Submit
    submit_question_button = driver.find_element(By.XPATH,'//*[@data-testid="send-button"]')
    if submit_question_button:
        submit_question_button.click()
    print("*"*100)
    print("please wait for the answer")
    print("*"*100)

def start_server():
    print("start_server is going to run!")
    driver = login()
    upload_image(driver)

if __name__ == '__main__':
    start_server()