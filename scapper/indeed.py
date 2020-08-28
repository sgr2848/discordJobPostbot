import requests
import selenium
import lxml
import json
from urllib import request
import re
from bs4 import BeautifulSoup
import time
from db_barell import get_db
from selenium.webdriver.firefox.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_job_object(posting_url):
    return_object = {}
    src = request.urlopen(posting_url).read()
    soup = BeautifulSoup(src,'lxml')
    return_object['job_title'] = soup.findAll('div', class_=re.compile('jobsearch-JobInfoHeader-title-container'))[0].get_text()
    # this give name and location of the company
    # return_object["company_name"] = soup.findAll('div', class_=re.compile(
    #     'icl-u-lg-mr--sm icl-u-xs-mr--xs'))[0].get_text()    
    rating_l_div = soup.findAll('div', class_=re.compile(
        'jobsearch-InlineCompanyRating'))[0]
    name_l = []
    for i in rating_l_div.findAll('div'):
        try:
            name_l.append(i.get_text())
        except:
            pass
    name_l = list(filter(None,name_l))
    if len(name_l) == 3:
        return_object['company_name'] = name_l[0]
        return_object['company_location'] = name_l[-1]
        return_object['reviews'] = "0 reviews"
    else:
        return_object['company_name'] = name_l[0]
        return_object['company_location'] = name_l[-1]
        return_object['reviews'] = name_l[1]
    try:
        apply_link = soup.find(id='applyButtonLinkContainer').find('a')['href']
        return_object['apply_link'] = apply_link
    except:
        print(f'{return_object["company_name"]} doesnt have apply link')
    return_object['job_description'] = soup.find('div', class_='jobsearch-jobDescriptionText').get_text()  
    return return_object
    
def run_indeed(limit=20):
    """
       limit<int> :  total number of job to add to db 
    """
    #remove comment for headless option
    # op = Options() 
    # op.headless = True
    # engine = selenium.webdriver.Firefox(options=op)
    #for gecko browser

    current_page = 1
    try:
        engine = selenium.webdriver.Firefox()
        #for chromium
        # engine = selenium.webdriver.Chrome()    
        engine.set_page_load_timeout(10)  #setting 10 sec timeout
        engine.get('https://www.indeed.com/')
        engine.find_element_by_xpath("//input[@id='text-input-what']").send_keys("Software engineer")
        engine.find_element_by_xpath(
            "//button[@class='icl-Button icl-Button--primary icl-Button--md icl-WhatWhere-button']").send_keys(Keys.ENTER)
        job_raw = WebDriverWait(engine, 2).until(EC.presence_of_element_located(
            (By.XPATH, "//td[@id='resultsCol']"))).get_attribute("innerHTML")
        job_raw = job_raw.split(" ")
        # print(job_raw)
        job_id_list =  []
        for i in job_raw:
            # the 
            if re.match('(^id="p_([a-z]|\d)+"$)|(^id="pj_([a-z]|\d)+"$)',i):            
                print(i[4:len(i)-1])
                job_id_list.append(i)
            else:
                pass
        del job_raw
        job_listing_sel_gen = [engine.find_element_by_xpath(f"//div[@id='{i[4:len(i)-1]}']//h2[@class='title']").find_element_by_tag_name("a") for i in job_id_list]
        del job_id_list
        job_href = [i.get_attribute("href") for i in job_listing_sel_gen]
        output_json = [] 
        with ThreadPoolExecutor(max_workers= 5) as executor:
            future = {executor.submit(get_job_object,i): i for i in job_href}
            for f in as_completed(future):
                output_json.append(f.result())
        json.dump(output_json,open("indeed.json","w"))
        engine.close()
    except Exception as e:
        print(e)
        engine.close()
if __name__ == "__main__":
    run_indeed()
