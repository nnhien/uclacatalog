'''
Parses the response from https://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details after sending a
request containing the subject area 
'''

from typing import List
from course import Course
from bs4 import BeautifulSoup
import api

def parse_catalog(resp: str, subj_area: str, div: str) -> List[Course]:
    if div == api.ALL_DIV: 
        return _get_all_div(resp, subj_area)
    else: 
        return _parse_course_list(resp, subj_area, div)

def _get_all_div(resp, subj_area):
    _parse_course_list(resp, subj_area, api.LOWER_DIV)
    _parse_course_list(resp, subj_area, api.UPPER_DIV)
    _parse_course_list(resp, subj_area, api.GRAD_DIV)

def _parse_course_list(resp, subj_area, div):
    course_list = []
    resp_soup = BeautifulSoup(resp.text, 'lxml')
    courses_soup = resp_soup.find('div', {'id': div}).find_all('div', class_='media-body')
    for course_soup in courses_soup:
        course = Course()
        course.dept = subj_area
        course.title = _parse_course_title(course_soup)
        course.ctlg_no = _parse_course_ctlg_no(course_soup)
        course.units = _parse_course_units(course_soup)
        course.desc = _parse_course_desc(course_soup)
        course_list.append(course)
    return course_list
        
def _parse_course_title(course_soup):
    return course_soup.h3.text.split('. ')[1]

def _parse_course_ctlg_no(course_soup):
    return course_soup.h3.text.split('. ')[0]

def _parse_course_units(course_soup):
    return course_soup.find_all('p')[0].text.split(': ')[1]

def _parse_course_desc(course_soup):
    return course_soup.find_all('p')[1].text