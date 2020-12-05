from selenium.webdriver.common.by import By
import hashlib
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.firefox.options import Options
import time
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request
import selenium
import lxml
import json
import re
from utils import shorten_url


HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Referer': 'https://cssspritegenerator.com',
          'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
          'Accept-Encoding': 'none',
          'Accept-Language': 'en-US,en;q=0.8',
          'Connection': 'keep-alive'}


def get_job_object(posting_url):
    return_object = {}
    request = urllib.request.Request(posting_url, None, HEADER)
    src = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(src, 'lxml')
    return_object['jobtitle'] = soup.findAll('div', class_=re.compile(
        'jobsearch-JobInfoHeader-title-container'))[0].get_text()
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
    name_l = list(filter(None, name_l))
    if len(name_l) == 3:
        return_object['companyname'] = name_l[0]
        return_object['companylocation'] = name_l[-1]
        # return_object['reviews'] = "0 reviews"
    else:
        return_object['companyname'] = name_l[0]
        return_object['companylocation'] = name_l[-1]
        # return_object['reviews'] = name_l[1]
    try:
        apply_link = soup.find(id='applyButtonLinkContainer').find('a')['href']
        return_object['applylink'] = shorten_url(apply_link)
    except:
        print(
            f'{return_object["companyname"]} doesnt have apply link - from Indeed')
        return 0
    return_object['jobdescription'] = soup.find(
        'div', class_='jobsearch-jobDescriptionText').get_text()
    low_des = return_object['applylink'].encode(
        'ascii', 'ignore')
    hash_text = hashlib.sha224(low_des).hexdigest()
    return_object["id"] = hash_text
    return_object["timestamps"] = datetime.now().timestamp()
    return return_object


def run_indeed():
    """
        conn : database connection
        limit<int> :  total number of job to add to db 
    """
    # remove comment for headless option
    # op = Options()
    # op.headless = True
    # engine = selenium.webdriver.Firefox(options=op)
    # for gecko browser
    engine = selenium.webdriver.Firefox()
    # for chromium

    # engine = selenium.webdriver.Chrome()
    # setting 10 sec timeout
    print("Current session is {}".format(engine.session_id))
    print("starting selenium for indeed")
    engine.set_page_load_timeout(10)
    current_page = 1
    try:

        engine.get('https://www.indeed.com/')
        time.sleep(3)
        try:
            engine.find_element_by_xpath(
                "//input[@id='text-input-what']").send_keys("Software engineer")
            engine.find_element_by_xpath(
                "//button[@class='icl-Button icl-Button--primary icl-Button--md icl-WhatWhere-button']").send_keys(Keys.ENTER)
            job_raw = WebDriverWait(engine, 5).until(EC.presence_of_element_located(
                (By.XPATH, "//td[@id='resultsCol']"))).get_attribute("innerHTML")
            job_raw = job_raw.split(" ")
            # print(job_raw)
            job_id_list = []
            for i in job_raw:
                # the
                if re.match('(^id="p_([a-z]|\d)+"$)|(^id="pj_([a-z]|\d)+"$)', i):
                    # print(i[4:len(i)-1])
                    job_id_list.append(i)
                else:
                    pass
            del job_raw
            job_listing_sel_gen = [engine.find_element_by_xpath(
                f"//div[@id='{i[4:len(i)-1]}']//h2[@class='title']").find_element_by_tag_name("a") for i in job_id_list]
            del job_id_list
            job_href = [i.get_attribute("href") for i in job_listing_sel_gen]
            print("closing selenium")
            engine.close()
            listing_collection = []

            with ThreadPoolExecutor(max_workers=5) as executor:
                future = {executor.submit(
                    get_job_object, i): i for i in job_href}
                for f in as_completed(future):
                    obj = f.result()
                    listing_collection.append(obj)
            listing_collection = list(
                filter(lambda x: x != 0, listing_collection))

            return listing_collection

        except Exception as e:
            print("Timeout")
            print(f"{e}")

    except Exception as e:
        print(f"{e} from indeed")
        print("closing selenium")


if __name__ == "__main__":
    run_indeed()
