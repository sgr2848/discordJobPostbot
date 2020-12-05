import requests
import json
import os
from dotenv import load_dotenv
load_dotenv(".env")


def shorten_url(url):
    '''
        API call to rebrandly and shorten the url
    '''
    linkRequest = {
        "destination": url, "domain": {"fullName": "rebrand.ly"}
    }
    API = os.environ.get("REBRANDLY_API")
    print(API)
    requestHeaders = {
        "Content-type": "application/json",
        "apikey": API,
    }

    r = requests.post("https://api.rebrandly.com/v1/links",
                      data=json.dumps(linkRequest),
                      headers=requestHeaders)

    if (r.status_code == requests.codes.ok):
        link = r.json()
        return link["shortUrl"]
    else:
        print(r.status_code)
