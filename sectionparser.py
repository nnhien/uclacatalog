'''
Parses the response from https://sa.ucla.edu/ro/public/soc after sending a request containing
the course and any filters into a list of Section objects
'''

from course import Course
from section import Section
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
import requests as req
import re
import time

def parse_sections(resp, course) -> List[Section]:
    out = []
    out.extend(_parse_root_sections(resp, course))
    return out

# Root sections can be both labs and lectures
def _parse_root_sections(resp, course):
    out = []
    sections_soup = BeautifulSoup(resp.text, 'lxml').find('div', {'id': re.compile('\\d*-children')})
    sections_arr = sections_soup.find_all("div", class_="class-info")
    for section_soup in sections_arr:
        section = Section()
        section.id = _parse_id(section_soup)
        section.enrollable = _parse_enrollable(section_soup)
        section.waitlistable = _parse_waitlistable(section_soup)
        section.enrolled = _parse_enrollment(section_soup)
        section.enrolled_max = _parse_enrollment_max(section_soup)
        section.waitlisted = _parse_waitlisted(section_soup)
        section.waitlisted_max = _parse_waitlisted_max(section_soup)
        section.meet_days = _parse_days(section_soup)
        section.start_time = str(_parse_start(section_soup))
        section.end_time = str(_parse_end(section_soup))
        section.location = _parse_location(section_soup)
        section.instructors = _parse_instructors(section_soup)
        section.last_updated = int(time.time())
        section.course = course
        out.append(section)
    return out

# Leaf sections can be both labs or discussions, or just may not exist
def _fetch_leaf_sections():
    NotImplemented

def _fetch_final():
    NotImplemented

def _parse_id(section_soup):
    # ID Attribute is in format of ID_subjAreaCLASSNUM; we want to split at '_' and take the first element
    return section_soup.div['id'].split("_")[0]

def _match_status(section_soup):
    status = section_soup.find("div", class_="statusColumn")

    # Use regex match groups to seperate openness from class capacity
    return re.findall("(Open|Closed|Waitlist)\\D*((\\d+ of \\d+ Enrolled)|(Class Full \\(\\d+\\))?)", status.text)[0]

def _parse_enrollable(section_soup):
    status = _match_status(section_soup)[0]
    return status == "Open"

def _parse_waitlistable(section_soup):
    status = _match_status(section_soup)[0]
    return status == "Waitlist"

''' 
For matching enrollment and waitlist, we only care about the numbers for matching. 

The result will always either come in a tuple containing (current_num, max_num) or an empty tuple if the course was closed by the department
'''
def _match_enrollment(section_soup):
    enrollment = _match_status(section_soup)[1]
    return re.findall('\\d+', enrollment)

def _parse_enrollment(section_soup):
    groups = _match_enrollment(section_soup)
    if len(groups) > 0: 
        return groups[0]
    else:
        return 0

def _parse_enrollment_max(section_soup):
    groups = _match_enrollment(section_soup)
    print(groups)
    if len(groups) > 1:
        return groups[1]
    elif len(groups) == 0:
        return 0
    else: 
        return groups[0]

def _match_waitlisted(section_soup):
    waitlist = section_soup.find("div", class_="waitlistColumn")
    return re.findall("\\d+", waitlist.text)

def _parse_waitlisted(section_soup):
    groups = _match_waitlisted(section_soup)
    if len(groups) > 0:
        return groups[0]
    else:
        return 0

def _parse_waitlisted_max(section_soup):
    groups = _match_waitlisted(section_soup)
    if len(groups) > 1:
        return groups[1]
    elif len(groups) == 0:
        return 0
    else:
        return groups[0]

def _parse_time(section_soup):
    time_soup = section_soup.find("div", class_="timeColumn")

    # Text comes in the format DAYS \n TIME, so we split it to give an array of [DAYS, TIME]
    return time_soup.text.split()

def _parse_days(section_soup):
    days = _parse_time(section_soup)[0]
    groups = re.findall("(M+)?(T+)?(W+)?(R+)?(F+)?", days)[0]
    
    # Filter for elements that aren't empty strings
    return list(filter(lambda e: e != '', groups))

def _parse_start_end(section_soup):
    time = _parse_time(section_soup)[1]
    return time.split('-') # time_arr is in format of [start_time, end_time]

def _parse_start(section_soup):
    start_str = _parse_start_end(section_soup)[0]
    return _parse_time_str(start_str)

def _parse_end(section_soup):
    end_str = _parse_start_end(section_soup)[1]
    return _parse_time_str(end_str)

def _parse_time_str(time_str):
    if time_str.find(':') > -1:
        # Time is within the hour
        return datetime.strptime(time_str, '%I:%M%p')
    else: 
        # Time *is* the hour; for some reason UCLA doesn't standardize timestamps and assumes that 12:00 = 12. We will follow this assumption grudgingly.
        return datetime.strptime(time_str, '%I%p')

def _parse_location(section_soup):
    return section_soup.find("div", class_="locationColumn").text.strip()

def _parse_instructors(section_soup):
    instructor_soup = section_soup.find("div", class_="instructorColumn")
    return [x for x in instructor_soup.p.contents if getattr(x, 'name', None) != 'br']
