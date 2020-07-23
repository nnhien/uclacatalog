class Course:
    def __init__(self):
        self.dept = ''
        self.ctlg_no = 0
        self.seq_no = ''
        self.title = ''
        self.desc = ''
        self.units = ''
        self.is_concurrent = False
        self.is_multi_listed = False
        self.token = ''

    def set_token(self):
        if self.dept == '' or self.ctlg_no == '':
            raise ValueError
        else:
            NotImplemented

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)