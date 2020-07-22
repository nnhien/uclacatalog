from typing import List
from course import Course
from section import Section
from filteroptions import FilterOptions
from urllib import parse as urlparser
import requests as req
import catalogparser

ALL_DIV = "all"
LOWER_DIV = "lower"
UPPER_DIV = "upper"
GRAD_DIV = "graduate"

# Note that courses do not include their sections; doing so by default is very
# resource intensive. If sections are desired, use the function below
def fetch_courses(subj_area: str, div: str = ALL_DIV) -> List[Course]:
    BASE = 'https://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details?'
    query = urlparser.urlencode({'SA': subj_area, 'funsel': '3'})
    return catalogparser.parse_catalog(req.get(BASE + query))

def fetch_sections(course: Course, options: FilterOptions) -> List[Section]:
    raise NotImplementedError