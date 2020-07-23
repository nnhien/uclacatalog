'''
Parses the response from https://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details after sending a
request containing the subject area 
'''

from typing import List
from course import Course
from bs4 import BeautifulSoup
import api
import re

def parse_catalog(resp: str, subj_area: str, div: str) -> List[Course]:
    if div == api.ALL_DIV: 
        return _get_all_div(resp, subj_area)
    else: 
        return _parse_course_list(resp, subj_area, div)

# TODO: Implement getting all divisions' courses asynchronously
# TODO: Perhaps also implement a more general function that takes in the response, subject area, and an array of divisions
def _get_all_div(resp, subj_area):
    return _parse_course_list(resp, subj_area, api.LOWER_DIV) + _parse_course_list(resp, subj_area, api.UPPER_DIV) + _parse_course_list(resp, subj_area, api.GRAD_DIV)

def _parse_course_list(resp, subj_area, div):
    course_list = []
    resp_soup = BeautifulSoup(resp.text, 'lxml')
    courses_soup = resp_soup.find('div', {'id': div}).find_all('div', class_='media-body')
    for course_soup in courses_soup:
        course = Course()
        course.subj_area = subj_area
        course.units = _parse_course_units(course_soup)
        course.desc = _parse_course_desc(course_soup)
        _parse_head(course, course_soup)
        course_list.append(course)
    return course_list
        

'''
Title and catalog numbers are enclosed in one h3 tag.

The Registrar specifies course numbering conventions at https://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Numbering-and-Description-Guide
Noteably:
- Courses that are credited concurrently between undergrad and grad are prefaced with C
- Courses that are administered between different departments are prefaced with M
- Courses that are individual study are appended with S, but if it's part of a sequence it's put before the sequence number
- C always comes before M

Therefore, the longest course number is CM999SC, but I haven't been able to find one with all the conventions.
'''
def _parse_head(course, course_soup):
    head = course_soup.h3.text.split('. ')
    ctlg_no = head[0]
    ctlg_no_components = re.findall('(C?)(M?)(\\d+)(\\D*)', ctlg_no)[0]
    course.title = _extract_course_title(head)
    course.is_concurrent = _extract_is_concurrent(ctlg_no_components)
    course.is_multi_listed = _extract_is_multi_listed(ctlg_no_components)
    course.ctlg_no = _extract_ctlg_no(ctlg_no_components)
    course.seq_no =  _extract_seq_no(ctlg_no_components)
    
def _extract_course_title(head):
    return head[1]

def _extract_is_concurrent(ctlg_no_comp):
    return ctlg_no_comp[0] != ''

def _extract_is_multi_listed(ctlg_no_comp):
    return ctlg_no_comp[1] != ''

def _extract_ctlg_no(ctlg_no_comp):
    return ctlg_no_comp[2]

def _extract_seq_no(ctlg_no_comp):
    return ctlg_no_comp[3]


'''
Course units is not always an integer (sometimes the registrar specifies a range like '1.0 to 4.0')

Format on the UCLA page is always 'Units: UNITS [to UNITS]'
'''
def _parse_course_units(course_soup):
    return course_soup.find_all('p')[0].text.split(': ')[1]

def _parse_course_desc(course_soup):
    return course_soup.find_all('p')[1].text