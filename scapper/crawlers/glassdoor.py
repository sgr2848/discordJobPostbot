import urllib.request
import selenium
from datetime import datetime
import lxml
import json
from utils import shorten_url
import re
import os
from bs4 import BeautifulSoup
import time
from selenium.webdriver.firefox.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import hashlib
import pickle


HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Referer': 'https://cssspritegenerator.com',
          'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
          'Accept-Encoding': 'none',
          'Accept-Language': 'en-US,en;q=0.8',
          'Connection': 'keep-alive'}


def get_job_objects(posting_url):
    # print(posting_url)
    # print("i")
    return_object = {}
    try:
        request = urllib.request.Request(posting_url, None, HEADER)
        src = urllib.request.urlopen(request).read()
        soup = BeautifulSoup(src, 'lxml',  from_encoding="iso-8859-1")
        cmpy_descrip = soup.findAll("div", class_=re.compile("css-ur1szg"))[0]
        # print(company_descrip)
        try:
            cmpy_descrip.span.decompose()
        except:
            print("cannot decompose - glassdoor posting_url")
        cmpy_desp_list = []
        for i in cmpy_descrip.findAll("div"):
            cmpy_desp_list.append(i.get_text())
        return_object['companyname'] = cmpy_desp_list[0]
        return_object['jobtitle'] = cmpy_desp_list[1]
        return_object['companylocation'] = cmpy_desp_list[2]
        return_object['applylink'] = shorten_url(posting_url)
        return_object["jobdescription"] = soup.find(
            'div', id="JobDescriptionContainer").get_text()
        low_des = return_object['applylink'].encode(
            'ascii', 'ignore')
        hash_text = hashlib.sha224(low_des).hexdigest()
        return_object["id"] = hash_text
        return_object["timestamps"] = datetime.now().timestamp()
        return return_object
    except Exception as e:
        print(e, "==Glassdoor")


def run_glassdoor():

    # https://www.glassdoor.com/Job/index.htm
    op = Options()
    op.headless = True
    engine = selenium.webdriver.Firefox(options=op)
    engine = selenium.webdriver.Firefox()

    # engine = selenium.webdriver.Chrome()
    print("Current session is {}".format(engine.session_id))
    engine.set_page_load_timeout(10)
    print("starting selenium for glassdoor")
    try:
        engine.get("https://www.glassdoor.com/Job/index.htm")
        engine.find_element_by_xpath(
            "//input[@id='KeywordSearch']").send_keys('software engineer')
        engine.find_element_by_xpath(
            "//button[@id='HeroSearchButton']").send_keys(Keys.ENTER)

        posting_ul_innerHTML = WebDriverWait(engine, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//ul[contains(@class,'jlGrid hover')]"))).find_elements_by_tag_name("a")
        posting_links = set()
        for i in posting_ul_innerHTML:
            link = i.get_attribute("href")

            if (link) and re.match("^(https://www.glassdoor.com/partner/jobListing.htm\?pos=\d{3}\&ao=\d{4,9}\&s=\d{2,3})+", link):
                # print(f"add ----  {link}",end="              ////\n")
                posting_links.add(link)
            else:
                pass
        print("closing selenium")
        engine.close()
        posting_links = list(posting_links)
        listing_collection = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            future = {executor.submit(get_job_objects, i)
                      for i in posting_links}
            for f in as_completed(future):
                listing_collection.append(f.result())
        with open('data.txt', 'w') as outfile:
            json.dump(listing_collection, outfile)
        return listing_collection

    except Exception as e:
        print(e)


if __name__ == "__main__":
    run_glassdoor()
