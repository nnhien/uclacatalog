from course import Course
import base64

class Event:
    def __init__(self):
        self.meet_days = []
        self.start_time = ''
        self.end_time = ''
        self.location = ''

class Final(Event):
    def __init__(self):
        super().__init__()

class Section(Event):
    def __init__(self):
        super().__init__()
        self.id = 0
        self.enrollable = False
        self.waitlistable = False
        self.enrolled = 0
        self.enrolled_max = 0
        self.waitlisted = 0
        self.waitlisted_max = 0
        self.instructors = []
        self.last_updated = 0
        self.course = None

    '''
    See course.py for full documentation on how the UCLA Registrar formats its tokens

    For course sections, tokens are used to fetch discussion sections. They follow mostly the same format as their course
    counterparts, with one difference:

    XXXXAABBID_DEPTXXXXABB
    
    Where ID is the section ID
    '''
    def get_token(self):
        if self.course.subj_area == '' or self.course.ctlg_no == '':
            raise ValueError
        else:
            # I am going to commit heresy and call a private function outside of its intended scope, 
            # but I don't feel like reimplementing function. Sue me.
            unencoded_token = self.course._get_full_ctlg_no() + self.id + "_" + self.course._get_path()
            unencoded_token_bytes = unencoded_token.encode('utf-8')
            base64_token = base64.standard_b64encode(unencoded_token_bytes)
            return base64_token.decode('utf-8')

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
