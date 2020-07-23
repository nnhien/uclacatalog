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

def parse_sections(resp) -> List[Section]:
    out = []
    sections_soup = BeautifulSoup(resp.text, 'lxml').find('div', {'id': re.compile('\\d*-children')})
    sections_arr = sections_soup.find_all("div", class_="class-info")
    for section_soup in sections_arr:
        section = Section()
        _parse_id(section, section_soup)
        _parse_status(section, section_soup)
        _parse_time(section, section_soup)
        _parse_location(section, section_soup)
        _parse_instructors(section, section_soup)
        section.last_updated = int(time.time())
        out.append(section)
    return out

def _parse_id(section, section_soup):
    # ID Attribute is in format of ID_subjAreaCLASSNUM; we want to split at '_' and take the first element
    section.id = section_soup.div['id'].split("_")[0]

def _parse_status(section, section_soup):
    # Collect relevant columns (UCLA for some reason doesn't include waitlist with status, but we will parse it in the same function for simplicity)
    status = section_soup.find("div", class_="statusColumn")
    waitlist = section_soup.find("div", class_="waitlistColumn")

    # Use regex match groups to seperate openness from class capacity
    groups = re.findall("(Open|Closed|Waitlist)((\\d+ of \\d+ Enrolled)|(Class Full \\(\\d+\\)))", status.text)[0]

    # Do parsing
    _parse_openness(section, groups[0])
    _parse_enrollment(section, groups[1])
    parse_waitlist(section, waitlist.text)

def _parse_openness(section, open):
    section.is_open = open == "Open"

''' 
For matching enrollment and waitlist, we only care about the numbers for matching. 
Also, there will always be an integer to match for (namely, 0)

The returned tuple always has the structure (current_amt, max_cap)
'''
def _parse_enrollment(section, enrollment):
    groups = re.findall("\\d+", enrollment)
    section.enrolled = groups[0]
    if len(groups) > 1:
        section.enrolled_max = groups[1]
    else:
        section.enrolled_max = groups[0]

def parse_waitlist(section, waitlist):
    groups = re.findall("\\d+", waitlist)
    section.waitlisted = groups[0]
    if len(groups) > 1:
        section.waitlisted_max = groups[1]
    else:
        section.waitlisted_max = groups[0]

def _parse_time(section, section_soup):
    time_soup = section_soup.find("div", class_="timeColumn")

    # Text comes in the format DAYS \n TIME, so we split it to give an array of [DAYS, TIME]
    time = time_soup.text.split()
    _parse_days(section, time[0])
    _parse_start_end(section, time[1])

def _parse_days(section, days):
    groups = re.findall("(M+)?(T+)?(W+)?(R+)?(F+)?", days)[0]
    
    # I'm bad at regex so filter for elements that aren't empty strings
    days = list(filter(lambda e: e != '', groups))
    section.meet_days.extend(days)

def _parse_start_end(event, time):
    time_arr = time.split('-') # time_arr is in format of [start_time, end_time]
    _parse_start(event, time_arr[0])
    _parse_end(event, time_arr[1])

def _parse_start(event, time_str):
    event.start_time = str(_parse_time_str(time_str))

def _parse_end(event, time_str):
    event.end_time = str(_parse_time_str(time_str))

def _parse_time_str(time_str):
    if time_str.find(':') > -1:
        # Time is within the hour
        return datetime.strptime(time_str, '%I:%M%p')
    else: 
        # Time *is* the hour; for some reason UCLA doesn't standardize timestamps and assumes that 12:00 = 12. We will follow this assumption grudgingly.
        return datetime.strptime(time_str, '%I%p')

def _parse_location(section, section_soup):
    location = section_soup.find("div", class_="locationColumn").text
    section.location = location.strip()

def _parse_instructors(section, section_soup):
    instructor_soup = section_soup.find("div", class_="instructorColumn")
    section.instructors = [x for x in instructor_soup.p.contents if getattr(x, 'name', None) != 'br']
