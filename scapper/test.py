from crawlers.indeed import get_job_object_sel

import unittest
import pprint
import json


def test_indeed_soup():
    obj = get_job_object_sel(
        'https://www.indeed.com/rc/clk?jk=4895c5581d575885&fccid=dd616958bd9ddc12&vjs=3')
    pprint.pprint(obj)


def test_glass_soup():
    obj = get_job_object_sel_glass(
        'https://www.glassdoor.com/job-listing/python-software-engineer-outcode-software-JV_IC3956718_KO0,24_KE25,41.htm?jl=3742123618&pos=103&ao=449986&s=58&guid=00000176340536e4accaf567bb182df5&src=GD_JOB_AD&t=SR&vt=w&cs=1_018866aa&cb=1607190525842&jobListingId=3742123618&ctt=1607248114849')


def test_indeed_sel():
    pass


def test_glass_sel():
    pass


if __name__ == "__main__":
    test_indeed_soup()
