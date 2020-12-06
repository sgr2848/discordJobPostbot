from selenium.webdriver.common.by import By
import hashlib
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.firefox.options import Options
import time
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import urllib.request
import selenium
import lxml
import json
import re
from .link_s import shorten_url


def get_job_object_sel(posting_url):
    '''
        Much more efficient in finding the elements but is slower than bs4
    '''
    return_object = {}
    op = Options()
    op.headless = True
    engine = selenium.webdriver.Firefox(options=op)
    engine.set_page_load_timeout(10)
    try:
        engine.get(posting_url)
        return_object['jobtitle'] = engine.find_element_by_xpath(
            "//h1[@class='icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title']").text
        name_addr = list(engine.find_element_by_xpath(
            "//div[@class='jobsearch-InlineCompanyRating icl-u-xs-mt--xs jobsearch-DesktopStickyContainer-companyrating']").find_elements_by_tag_name("div"))
        if len(name_addr) == 3:
            return_object['companyname'] = name_addr[0].text
            return_object['companylocation'] = name_addr[-1].text
            # return_object['reviews'] = "0 reviews"
        else:
            return_object['companyname'] = name_addr[0].text
            return_object['companylocation'] = name_addr[-1].text
        return_object['jobdescription'] = engine.find_element_by_xpath(
            "//div[@id='jobDescriptionText']").text
        try:
            apply_button = list(engine.find_element_by_xpath(
                "//div[@id='applyButtonLinkContainer']").find_elements_by_tag_name('a'))
            return_object['applylink'] = shorten_url(
                apply_button[0].get_attribute('href'))
            low_des = return_object['applylink'].encode(
                'ascii', 'ignore')
            hash_text = hashlib.sha224(low_des).hexdigest()
            return_object["id"] = hash_text
        except Exception as err:
            return_object['applylink'] = shorten_url(posting_url)
            low_des = return_object['applylink'].encode(
                'ascii', 'ignore')
            hash_text = hashlib.sha224(low_des).hexdigest()
            return_object["id"] = hash_text
        now = datetime.now(timezone.utc)
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
        posix_timestamp_micros = (now - epoch) // timedelta(microseconds=1)
        posix_timestamp_millis = posix_timestamp_micros // 1000
        return_object["timestamps"] = posix_timestamp_millis
    except Exception as err:
        print(err)
        engine.close()

    engine.close()
    return return_object


def get_job_object(posting_url):
    HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Referer': 'https://cssspritegenerator.com',
              'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
              'Accept-Encoding': 'none',
              'Accept-Language': 'en-US,en;q=0.8',
              'Connection': 'keep-alive'}
    return_object = {}
    request = urllib.request.Request(posting_url, None, HEADER)
    src = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(src, 'lxml')
    return_object['jobtitle'] = soup.findAll('div', class_=re.compile(
        'jobsearch-JobInfoHeader-title-container'))[0].get_text()
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
    try:
        apply_link = soup.find(
            "div", id='applyButtonLinkContainer').find('a')['href']
        return_object['applylink'] = shorten_url(apply_link)
        print(apply_link)
        low_des = return_object['applylink'].encode(
            'ascii', 'ignore')
        hash_text = hashlib.sha224(low_des).hexdigest()
        return_object["id"] = hash_text

    except Exception as err:
        return_object['applylink'] = shorten_url(posting_url)
        low_des = return_object['applylink'].encode(
            'ascii', 'ignore')
        hash_text = hashlib.sha224(low_des).hexdigest()
        return_object["id"] = hash_text

    return_object['jobdescription'] = soup.find(
        'div', class_='jobsearch-jobDescriptionText').get_text()
    now = datetime.now(timezone.utc)
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    posix_timestamp_millis = posix_timestamp_micros // 1000
    return_object["timestamps"] = posix_timestamp_millis
    return return_object


def run_indeed(use_sel=False):
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
            if not use_sel:
                with ThreadPoolExecutor(max_workers=5) as executor:
                    future = {executor.submit(
                        get_job_object, i): i for i in job_href}
                    for f in as_completed(future):
                        obj = f.result()
                        listing_collection.append(obj)

            else:
                with ThreadPoolExecutor(max_workers=5) as executor:
                    future = {executor.submit(
                        get_job_object_sel, i): i for i in job_href}
                    for f in as_completed(future):
                        obj = f.result()
                        listing_collection.append(obj)

            listing_collection = list(
                filter(lambda x: x != 0, listing_collection))
            print("INDEED RETURNING COLLECTION")
            return listing_collection
        except Exception as e:
            print("Some err")
            print(f"{e}")

    except Exception as e:
        print(f"{e} from indeed")
        print("closing selenium")
