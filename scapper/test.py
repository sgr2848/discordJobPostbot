from crawlers.indeed import get_job_object_sel
import unittest
import pprint
import json


def test_indeed_soup():
    obj = get_job_object_sel(
        'https://www.indeed.com/rc/clk?jk=4895c5581d575885&fccid=dd616958bd9ddc12&vjs=3')
    pprint.pprint(obj)


def test_glass_soup():
    pass


def test_indeed_sel():
    pass


def test_glass_sel():
    pass


if __name__ == "__main__":
    test_indeed_soup()
