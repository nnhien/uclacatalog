from typing import List
from course import Course
from section import Section
from filteroptions import FilterOptions
from urllib import parse as urlparser
import requests as req
import catalogparser
import sectionparser

ALL_DIV = "all"
LOWER_DIV = "lower"
UPPER_DIV = "upper"
GRAD_DIV = "graduate"

# Note that courses do not include their sections; doing so by default is very
# resource intensive. If sections are desired, use the function below
def fetch_courses(subj_area: str, div: str = ALL_DIV) -> List[Course]:
    BASE = 'https://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details?'
    query = urlparser.urlencode({'SA': subj_area, 'funsel': '3'})
    return catalogparser.parse_catalog(req.get(BASE + query), subj_area, div)

def fetch_sections(course: Course, options: FilterOptions, term: str) -> List[Section]:
    default_filters = '{"enrollment_status":"O,W,C,X,T,S","advanced":"y","meet_days":"M,T,W,R,F","start_time":"8:00 am","end_time":"8:00 pm","meet_locations":null,"meet_units":null,"instructor":null,"class_career":null,"impacted":null,"enrollment_restrictions":null,"enforced_requisites":null,"individual_studies":null,"summer_session":null}'
    BASE = 'https://sa.ucla.edu/ro/Public/SOC/Results/GetCourseSummary?'
    query = urlparser.urlencode({'model': course.get_json_model(term), 'FilterFlags': default_filters})
    return sectionparser.parse_sections(req.get(BASE + query))