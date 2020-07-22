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

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
