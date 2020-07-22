from typing import List
from course import Course
from bs4 import BeautifulSoup

def parse_catalog(response) -> List[Course]:
    catalog = []
    resp_soup = BeautifulSoup(response.text)
    print(resp_soup)
    return catalog

