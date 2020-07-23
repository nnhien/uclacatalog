from typing import List
from course import Course
from section import Section
from filteroptions import FilterOptions
import catalogparser
import sectionparser
import requesthandler

ALL_DIV = "all"
LOWER_DIV = "lower"
UPPER_DIV = "upper"
GRAD_DIV = "graduate"

# Note that courses do not include their sections; doing so by default is very
# resource intensive. If sections are desired, use the function below
def fetch_courses(subj_area: str, div: str = ALL_DIV) -> List[Course]:
    return catalogparser.parse_catalog(requesthandler.fetch_courses(subj_area, div), subj_area, div)

def fetch_sections(course: Course, options: FilterOptions, term: str) -> List[Section]:
    return sectionparser.parse_sections(requesthandler.fetch_root_sections(course, options, term), course, term)