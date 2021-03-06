from typing import List
from .model import Course, Section
from .parser import catalogparser, sectionparser
from . import requesthandler

ALL_DIV = "all"
LOWER_DIV = "lower"
UPPER_DIV = "upper"
GRAD_DIV = "graduate"

LEGAL_SA = {
    "AERO ST",
    "AF AMER",
    "AFRC ST",
    "AM IND",
    "ASL",
    "AN N EA",
    "ANES",
    "ANTHRO",
    "APPLING",
    "ARABIC",
    "ARCHEOL",
    "ARCH&UD",
    "ARMENIA",
    "ART",
    "ART HIS",
    "ART&ARC",
    "ARTS ED",
    "ASIAN",
    "ASIA AM",
    "ASTR",
    "A&O SCI",
    "BIOENGR",
    "BIOINFO",
    "BIOINFR",
    "BIOL CH",
    "BIOMATH",
    "BMD RES",
    "BIOSTAT",
    "C&EE ST",
    "CH ENGR",
    "CHEM",
    "CHICANO",
    "CHIN",
    "C&EE",
    "CLASSIC",
    "CLUSTER",
    "COMM",
    "CESC",
    "COM HLT",
    "COM LIT",
    "C&S BIO",
    "COM SCI",
    "CAEM",
    "DANCE",
    "DENT",
    "DESMA",
    "DGT HUM",
    "DIS STD",
    "DUTCH",
    "EPS SCI",
    "EA STDS",
    "EE BIOL",
    "ECON",
    "EDUC",
    "EC ENGR",
    "ENGR",
    "ENGL",
    "ESL",
    "ENGCOMP",
    "ENVIRON",
    "ENV HLT",
    "EPIDEM",
    "ETHNMUS",
    "FILIPNO",
    "FILM TV",
    "FOOD ST",
    "FRNCH",
    "GENDER",
    "GEOG",
    "GERMAN",
    "GRNTLGY",
    "GLB HLT",
    "GJ STDS",
    "GLBL ST",
    "GRAD PD",
    "GREEK",
    "HLT POL",
    "HEBREW",
    "HIN-URD",
    "HIST",
    "HNRS",
    "HUM GEN",
    "HNGAR",
    "IL AMER",
    "I E STD",
    "INDO",
    "INF STD",
    "I A STD",
    "INTL DV",
    "I M STD",
    "IRANIAN",
    "ISLM ST",
    "ITALIAN",
    "JAPAN",
    "JEWISH",
    "KOREA",
    "LBR STD",
    "LATIN",
    "LATN AM",
    "LAW",
    "UG-LAW",
    "LGBTQS",
    "LIFESCI",
    "LING",
    "MGMT",
    "MGMTEX",
    "MGMTFT",
    "MGMTFE",
    "MGMTGEX",
    "MGMTMFE",
    "MGMTMSA",
    "MGMTPHD",
    "MAT SCI",
    "MATH",
    "MECH&AE",
    "MED",
    "MIMG",
    "M E STD",
    "MIL SCI",
    "M PHARM",
    "MOL BIO",
    "MOL TOX",
    "MCD BIO",
    "MC&IP",
    "MUSC",
    "MSC IND",
    "MUSCLG",
    "NAV SCI",
    "NR EAST",
    "NEURBIO",
    "NEURLGY",
    "NEURO",
    "NEUROSC",
    "NEURSGY",
    "NURSING",
    "OBGYN",
    "OPTH",
    "ORL BIO",
    "ORTHPDC",
    "PATH",
    "PEDS",
    "PHILOS",
    "PHYSICS",
    "PBMED",
    "PHYSCI",
    "PHYSIOL",
    "POLSH",
    "POL SCI",
    "PORTGSE",
    "COMPTNG",
    "PSYCTRY",
    "PSYCH",
    "PUB AFF",
    "PUB HLT",
    "PUB PLC",
    "RAD ONC",
    "RELIGN",
    "ROMANIA",
    "RUSSN",
    "SCAND",
    "SCI EDU",
    "SEMITIC",
    "SRB CRO",
    "SLAVC",
    "SOC SC",
    "SOC THT",
    "SOC WLF",
    "SOC GEN",
    "SOCIOL",
    "S ASIAN",
    "SEASIAN",
    "SPAN",
    "STATS",
    "SURGERY",
    "SWAHILI",
    "THAI",
    "THEATER",
    "TURKIC",
    "UNIV ST",
    "URBN PL",
    "UROLOGY",
    "VIETMSE",
    "WL ARTS",
    "YIDDSH"
}

# Returns a list of all courses in the specified division for the specified subject area
def fetch_catalog(subj_area: str, div: str = ALL_DIV) -> List[Course]:
    subj_area = subj_area.upper()
    if subj_area in LEGAL_SA:
        return catalogparser.parse_catalog(requesthandler.fetch_courses(subj_area, div), subj_area, div)
    else:
        raise ValueError(subj_area + ' not a legal subject area!')

# Returns list of courses in the specified subject area with a matching inputted catalog number
def fetch_matching_courses(subj_area: str, ctlg_no: str) -> List[Course]:
    subj_area = subj_area.upper()
    if subj_area in LEGAL_SA:
        return catalogparser.find_course(requesthandler.fetch_courses(subj_area, ALL_DIV), subj_area, ctlg_no)
    else:
        raise ValueError(subj_area + ' not a legal subject area!')

# Returns a list of root level sections for the specified course, or an empty list if no sections could be found
def fetch_sections(course: Course, term: str) -> List[Section]:
    return sectionparser.parse_sections(requesthandler.fetch_root_sections(course, term), course, term)