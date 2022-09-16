import re
from typing import List, Tuple

from bs4 import BeautifulSoup, ResultSet
from requests import Response
from uclacatalog import api
from uclacatalog.model import Course

'''
Parser for responses from https://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details
'''


def parse_catalog(resp: Response, subj_area: str, div: str) -> List[Course]:
    if div == api.ALL_DIV:
        return _get_all_div(resp, subj_area)
    else:
        return _parse_course_list(resp, subj_area, div)


def find_course(resp: Response, subj_area: str, ctlg_no: str) -> List[Course]:
    resp_soup = BeautifulSoup(resp.text, 'lxml')
    courses_soup = resp_soup.find_all('div', class_='media-body')
    matched_courses = []
    for course_soup in courses_soup:
        course_head_soup = course_soup.h3
        if ctlg_no in course_head_soup.text:
            course = _populate_course(course_soup, subj_area)
            matched_courses.append(course)
    return matched_courses


# TODO: Implement getting all divisions' courses asynchronously
# TODO: Perhaps also implement a more general function that takes in the response, subject area, and an array of divisions
def _get_all_div(resp: Response, subj_area: str) -> List[Course]:
    return _parse_course_list(resp, subj_area, api.LOWER_DIV) + _parse_course_list(resp, subj_area, api.UPPER_DIV) + _parse_course_list(resp, subj_area, api.GRAD_DIV)


def _parse_course_list(resp: Response, subj_area: str, div: str) -> List[Course]:
    course_list = []
    resp_soup = BeautifulSoup(resp.text, 'lxml')
    # FIXME: This is the line that's stopped working
    courses_soup = resp_soup.find('div', {'id': div}).find_all(  # type: ignore
        'div', class_='media-body')
    for course_soup in courses_soup:
        course = _populate_course(course_soup, subj_area)
        course_list.append(course)
    return course_list


def _populate_course(course_soup: ResultSet, subj_area: str) -> Course:
    course = Course()
    course.subj_area = subj_area
    course.units = _parse_course_units(course_soup)
    course.desc = _parse_course_desc(course_soup)
    _parse_head(course, course_soup)
    return course


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


def _split_head(course_soup: ResultSet) -> List[str]:
    return course_soup.h3.text.split('. ')  # type: ignore


def _match_ctlg_no_components(ctlg_no: str) -> Tuple[str, ...]:
    return re.findall('(C?)(M?)(\\d+)(\\D*)', ctlg_no)[0]


def _parse_head(course: Course, course_soup: ResultSet) -> None:
    head = _split_head(course_soup)
    ctlg_no = head[0]

    '''
    The resultant tuple takes the form

    (is_concurrent, is_multilisted, ctlg_no, seq_no)
    '''
    ctlg_no_components = _match_ctlg_no_components(ctlg_no)
    course.title = _extract_course_title(head)
    course.is_concurrent = _extract_is_concurrent(ctlg_no_components)
    course.is_multi_listed = _extract_is_multi_listed(ctlg_no_components)
    course.ctlg_no = _extract_ctlg_no(ctlg_no_components)
    course.seq_no = _extract_seq_no(ctlg_no_components)


def _extract_course_title(head: List[str]) -> str:
    return head[1]


def _extract_is_concurrent(ctlg_no_comp: Tuple[str, ...]) -> bool:
    return ctlg_no_comp[0] != ''


def _extract_is_multi_listed(ctlg_no_comp: Tuple[str, ...]) -> bool:
    return ctlg_no_comp[1] != ''


def _extract_ctlg_no(ctlg_no_comp: Tuple[str, ...]) -> str:
    return ctlg_no_comp[2]


def _extract_seq_no(ctlg_no_comp: Tuple[str, ...]) -> str:
    return ctlg_no_comp[3]


'''
Course units is not always an integer (sometimes the registrar specifies a range like '1.0 to 4.0')

Format on the UCLA page is always 'Units: UNITS [to UNITS]'
'''


# NOTE: Based on pylance's type hinting, I would assume course_soup is
# type bs4.ResultSet, but find_all doesn't seem to be a member function
# of it, so IDK.
def _parse_course_units(course_soup: ResultSet) -> str:
    return course_soup.find_all('p')[0].text.split(': ')[1]  # type: ignore


def _parse_course_desc(course_soup: ResultSet) -> str:
    return course_soup.find_all('p')[1].text  # type: ignore
