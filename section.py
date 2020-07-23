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
        self.is_open = False
        self.enrolled = 0
        self.enrolled_max = 0
        self.waitlisted = 0
        self.waitlisted_max = 0
        self.final = Final()
        self.instructors = []
        self.last_updated = 0


    '''
    See course.py for full documentation on how the UCLA Registrar formats its tokens

    For course sections, tokens are used to fetch discussion sections. They follow mostly the same format as their course
    counterparts, with one difference:

    XXXXA BBID_DEPTXXXXABB
    
    Where ID is the section ID
    '''
    def get_token(self):
        NotImplemented

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
