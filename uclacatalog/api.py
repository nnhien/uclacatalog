import enum
from typing import List, Union

from . import requesthandler
from .model import Course, Section
from .parser import catalogparser, sectionparser

# Keep these around for backwards compatibility, probably
ALL_DIV = "all"
LOWER_DIV = "lower"
UPPER_DIV = "upper"
GRAD_DIV = "graduate"


# Added this as a better practice to module-level constants
# Enums are more intuitive and easier to filter with IntelliSense
class Division(enum.Enum):
    """Enum of course divisions to filter by."""
    ALL = ALL_DIV
    LOWER = LOWER_DIV
    UPPER = UPPER_DIV
    GRAD = GRAD_DIV


# Keep this around for backwards compatibility, probably
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


# Added this as a better practice to constants in a module-level set
# whose contents cannot be previewed without looking at documentation
# Enums are more intuitive and easier to filter with IntelliSense
class Subject(enum.Enum):
    """Enum of valid subject areas to search for.

    Due to limitations on how variables can be named, the enum member
    name for a given class code has spaces, &, and - replaced with the
    underscore (_) character. Some examples include:

        - Subject.ART_ARC.value == "ART&ARC"
        - Subject.C_S_BIO.value == "C&S BIO"
        - Subject.HIN_URD.value == "HIN-URD"
    """
    AERO_ST = "AERO ST"
    AF_AMER = "AF AMER"
    AFRC_ST = "AFRC ST"
    AM_IND = "AM IND"
    ASL = "ASL"
    AN_N_EA = "AN N EA"
    ANES = "ANES"
    ANTHRO = "ANTHRO"
    APPLING = "APPLING"
    ARABIC = "ARABIC"
    ARCHEOL = "ARCHEOL"
    ARCH_UD = "ARCH&UD"
    ARMENIA = "ARMENIA"
    ART = "ART"
    ART_HIS = "ART HIS"
    ART_ARC = "ART&ARC"
    ARTS_ED = "ARTS ED"
    ASIAN = "ASIAN"
    ASIA_AM = "ASIA AM"
    ASTR = "ASTR"
    A_O_SCI = "A&O SCI"
    BIOENGR = "BIOENGR"
    BIOINFO = "BIOINFO"
    BIOINFR = "BIOINFR"
    BIOL_CH = "BIOL CH"
    BIOMATH = "BIOMATH"
    BMD_RES = "BMD RES"
    BIOSTAT = "BIOSTAT"
    C_EE_ST = "C&EE ST"
    CH_ENGR = "CH ENGR"
    CHEM = "CHEM"
    CHICANO = "CHICANO"
    CHIN = "CHIN"
    C_EE = "C&EE"
    CLASSIC = "CLASSIC"
    CLUSTER = "CLUSTER"
    COMM = "COMM"
    CESC = "CESC"
    COM_HLT = "COM HLT"
    COM_LIT = "COM LIT"
    C_S_BIO = "C&S BIO"
    COM_SCI = "COM SCI"
    CAEM = "CAEM"
    DANCE = "DANCE"
    DENT = "DENT"
    DESMA = "DESMA"
    DGT_HUM = "DGT HUM"
    DIS_STD = "DIS STD"
    DUTCH = "DUTCH"
    EPS_SCI = "EPS SCI"
    EA_STDS = "EA STDS"
    EE_BIOL = "EE BIOL"
    ECON = "ECON"
    EDUC = "EDUC"
    EC_ENGR = "EC ENGR"
    ENGR = "ENGR"
    ENGL = "ENGL"
    ESL = "ESL"
    ENGCOMP = "ENGCOMP"
    ENVIRON = "ENVIRON"
    ENV_HLT = "ENV HLT"
    EPIDEM = "EPIDEM"
    ETHNMUS = "ETHNMUS"
    FILIPNO = "FILIPNO"
    FILM_TV = "FILM TV"
    FOOD_ST = "FOOD ST"
    FRNCH = "FRNCH"
    GENDER = "GENDER"
    GEOG = "GEOG"
    GERMAN = "GERMAN"
    GRNTLGY = "GRNTLGY"
    GLB_HLT = "GLB HLT"
    GJ_STDS = "GJ STDS"
    GLBL_ST = "GLBL ST"
    GRAD_PD = "GRAD PD"
    GREEK = "GREEK"
    HLT_POL = "HLT POL"
    HEBREW = "HEBREW"
    HIN_URD = "HIN-URD"
    HIST = "HIST"
    HNRS = "HNRS"
    HUM_GEN = "HUM GEN"
    HNGAR = "HNGAR"
    IL_AMER = "IL AMER"
    I_E_STD = "I E STD"
    INDO = "INDO"
    INF_STD = "INF STD"
    I_A_STD = "I A STD"
    INTL_DV = "INTL DV"
    I_M_STD = "I M STD"
    IRANIAN = "IRANIAN"
    ISLM_ST = "ISLM ST"
    ITALIAN = "ITALIAN"
    JAPAN = "JAPAN"
    JEWISH = "JEWISH"
    KOREA = "KOREA"
    LBR_STD = "LBR STD"
    LATIN = "LATIN"
    LATN_AM = "LATN AM"
    LAW = "LAW"
    UG_LAW = "UG-LAW"
    LGBTQS = "LGBTQS"
    LIFESCI = "LIFESCI"
    LING = "LING"
    MGMT = "MGMT"
    MGMTEX = "MGMTEX"
    MGMTFT = "MGMTFT"
    MGMTFE = "MGMTFE"
    MGMTGEX = "MGMTGEX"
    MGMTMFE = "MGMTMFE"
    MGMTMSA = "MGMTMSA"
    MGMTPHD = "MGMTPHD"
    MAT_SCI = "MAT SCI"
    MATH = "MATH"
    MECH_AE = "MECH&AE"
    MED = "MED"
    MIMG = "MIMG"
    M_E_STD = "M E STD"
    MIL_SCI = "MIL SCI"
    M_PHARM = "M PHARM"
    MOL_BIO = "MOL BIO"
    MOL_TOX = "MOL TOX"
    MCD_BIO = "MCD BIO"
    MC_IP = "MC&IP"
    MUSC = "MUSC"
    MSC_IND = "MSC IND"
    MUSCLG = "MUSCLG"
    NAV_SCI = "NAV SCI"
    NR_EAST = "NR EAST"
    NEURBIO = "NEURBIO"
    NEURLGY = "NEURLGY"
    NEURO = "NEURO"
    NEUROSC = "NEUROSC"
    NEURSGY = "NEURSGY"
    NURSING = "NURSING"
    OBGYN = "OBGYN"
    OPTH = "OPTH"
    ORL_BIO = "ORL BIO"
    ORTHPDC = "ORTHPDC"
    PATH = "PATH"
    PEDS = "PEDS"
    PHILOS = "PHILOS"
    PHYSICS = "PHYSICS"
    PBMED = "PBMED"
    PHYSCI = "PHYSCI"
    PHYSIOL = "PHYSIOL"
    POLSH = "POLSH"
    POL_SCI = "POL SCI"
    PORTGSE = "PORTGSE"
    COMPTNG = "COMPTNG"
    PSYCTRY = "PSYCTRY"
    PSYCH = "PSYCH"
    PUB_AFF = "PUB AFF"
    PUB_HLT = "PUB HLT"
    PUB_PLC = "PUB PLC"
    RAD_ONC = "RAD ONC"
    RELIGN = "RELIGN"
    ROMANIA = "ROMANIA"
    RUSSN = "RUSSN"
    SCAND = "SCAND"
    SCI_EDU = "SCI EDU"
    SEMITIC = "SEMITIC"
    SRB_CRO = "SRB CRO"
    SLAVC = "SLAVC"
    SOC_SC = "SOC SC"
    SOC_THT = "SOC THT"
    SOC_WLF = "SOC WLF"
    SOC_GEN = "SOC GEN"
    SOCIOL = "SOCIOL"
    S_ASIAN = "S ASIAN"
    SEASIAN = "SEASIAN"
    SPAN = "SPAN"
    STATS = "STATS"
    SURGERY = "SURGERY"
    SWAHILI = "SWAHILI"
    THAI = "THAI"
    THEATER = "THEATER"
    TURKIC = "TURKIC"
    UNIV_ST = "UNIV ST"
    URBN_PL = "URBN PL"
    UROLOGY = "UROLOGY"
    VIETMSE = "VIETMSE"
    WL_ARTS = "WL ARTS"
    YIDDSH = "YIDDSH"


def _validate_subject(subj_area: Union[Subject, str]) -> str:  # type: ignore
    """Validate an input subject and return it as an uppercase string.

    Args:
        subj_area (Union[Subject, str]): The client's input to
        functions requiring a subject area argument.

    Raises:
        ValueError: Param subj_area is not a legal subject area.

    Returns:
        str: The subject's code (e.g. COM SCI) as an uppercase string.
    """
    # Normalize subject arg: keep str option for backwards compatibility
    if isinstance(subj_area, Subject):
        subj_area: str = subj_area.value
    else:
        subj_area = subj_area.upper()

    # Validate subject area
    try:
        # Checks enum's internal mapping
        # Should be O(1) like checking LEGAL_SA
        Subject(subj_area)
    except ValueError:
        raise ValueError(subj_area + ' not a legal subject area!') from None
    return subj_area


def fetch_catalog(subj_area: Union[Subject, str],  # type: ignore
                  div: Union[Division, str] = Division.ALL  # type: ignore
                  ) -> List[Course]:
    """Return a list of all courses in specified subject and division.

    Args:
        subj_area (Union[Subject, str]): Specified subject area.
        div (Union[Division, str], optional): Specified division.
        Defaults to fetching all divisions.

    Returns:
        List[Course]: The requested courses.
    """
    # Normalize args
    subj_area = _validate_subject(subj_area)
    if isinstance(div, Division):
        div: str = div.value

    # Fetch and parse
    courses_resp = requesthandler.fetch_courses(subj_area, div)
    return catalogparser.parse_catalog(courses_resp, subj_area, div)


def fetch_matching_courses(subj_area: Union[Subject, str],
                           ctlg_no: str
                           ) -> List[Course]:
    """Return list of courses matching inputted subject and number.

    Args:
        subj_area (Union[Subject, str]): Specified subject area.
        ctlg_no (str): Catalog number to match.

    Returns:
        List[Course]: The matching courses.
    """
    subj_area = _validate_subject(subj_area)
    courses_resp = requesthandler.fetch_courses(subj_area, Division.ALL)
    return catalogparser.find_course(courses_resp, subj_area, ctlg_no)


def fetch_sections(course: Course, term: str) -> List[Section]:
    """Return a list of root level sections for the specified course.

    Args:
        course (Course): Specified course.
        term (str): Specified term.

    Returns:
        List[Section]: Root level sections for the specified course.
        Returns an empty list if no sections could be found.
    """
    return sectionparser.parse_sections(requesthandler.fetch_root_sections(course, term), course, term)
