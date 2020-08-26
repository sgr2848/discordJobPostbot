import requests
import selenium
import time,os
from dotenv import load_dotenv 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'), verbose=True)
SQL_CRED = os.environ.get("ENDPOINT")
def run_indeed():
    #remove comment for headless option
    # op = Options() 
    # op.headless = True
    # engine = selenium.webdriver.Firefox(options=op)
    #for gecko browser
    engine = selenium.webdriver.Firefox()
    #for chromium
    # engine = selenium.webdriver.Chrome()
    engine.set_page_load_timeout(10)  #setting 10 sec timeout
    engine.get('https://www.indeed.com/')
    engine.find_element_by_xpath("//input[@id='text-input-what']").send_keys("Software engineer")
    engine.find_element_by_xpath(
        "//button[@class='icl-Button icl-Button--primary icl-Button--md icl-WhatWhere-button']").send_keys(Keys.ENTER)
if __name__ == "__main__":
    run_indeed()
