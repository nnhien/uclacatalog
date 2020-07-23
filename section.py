from course import Course
import base64
import json

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
        self.course = None
        self.id = 0
        self.sec_no = 0
        self.term = ''
        self.enrollable = False
        self.waitlistable = False
        self.enrolled = 0
        self.enrolled_max = 0
        self.waitlisted = 0
        self.waitlisted_max = 0
        self.instructors = []
        self.final = Final()
        self.last_updated = 0

    def to_jsons(self):
        json_obj = json.loads(self.course.to_jsons(self.term))
        json_obj['IsRoot'] = False
        json_obj['SessionGroup'] = None
        json_obj['ClassNumber'] = self.sec_no
        json_obj['SequenceNumber'] = '1'
        json_obj['Path'] = self._get_path()
        json_obj['Token'] = self.get_token()

        return json.dumps(json_obj)

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
            unencoded_token = self.course.get_full_ctlg_no() + self._get_path()
            unencoded_token_bytes = unencoded_token.encode('utf-8')
            base64_token = base64.standard_b64encode(unencoded_token_bytes)
            return base64_token.decode('utf-8')

    def _get_path(self):
        # This feels so dirty
        return self.id + "_" + self.course.get_path()

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
