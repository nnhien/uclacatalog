class Course:
    def __init__(self):
        self.dept = ''
        self.ctlg_no = ''
        self.desc = ''
        self.units = 0.0

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)