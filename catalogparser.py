'''
Parses the response from https://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details after sending a
request containing the subject area 
'''

from typing import List
from course import Course
from bs4 import BeautifulSoup

def parse_catalog(response: str, subj_area: str, div: str) -> List[Course]:
    catalog = []
    resp_soup = BeautifulSoup(response.text)
    print(resp_soup)
    return catalog