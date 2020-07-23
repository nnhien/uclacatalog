import base64
import json

class Course:
    def __init__(self):
        self.subj_area = ''
        self.ctlg_no = ''
        self.seq_no = ''
        self.title = ''
        self.desc = ''
        self.units = ''
        self.is_concurrent = False
        self.is_multi_listed = False

    '''
    The schedule of classes backend requires a query with a JSON Object to request the sections of a course

    The JSON Object takes the form of:
    {
        "Term": XXQ, // Where XX is the last two digits of the academic year and Q is the quarter (S for spring, W for winter, 
                     // F for fall, 1 for Summer session.)
        "SubjectAreaCode": self.subj_area,
        "CatalogNumber": XXXXAABB, // See token specification
        "IsRoot": true/false, // true if requesting lecture sections, false if requesting discussion sections

        // For the next three, the values are always the same. I'm not sure what their purpose is, but they're required in the object
        // or else the request will fail.
        "SessionGroup": "%",
        "ClassNumber": "%",
        "SequenceNumber": null,
        
        "Path": DEPTAABB, // See token specification
        "MultiListedClassFlag": "y/n" // Depends on the value of self.is_multi_listed
        "Token": get_token() // See below for token format
    }
    '''
    def get_json_model(self, term: str):
        class_flag = 'n'
        if self.is_multi_listed: class_flag = 'y'
        return json.dumps(
            {
                'Term': term,
                'SubjectAreaCode': self.subj_area,
                'CatalogNumber': self._get_full_ctlg_no(),
                'IsRoot': True,
                'SessionGroup': '%',
                'ClassNumber': '%',
                'SequenceNumber': None,
                'Path': self._get_path(),
                'MultiListedClassFlag': class_flag,
                'Token': self.get_token()
            }
        )

    '''
    The schedule of classes backend requires a token to request the sections of a course

    A course's token is a Base64 encoded string that takes the form:

        XXXXAABBDEPTXXXXAABB
    
    Where:
    - XXXX is the catalog number, zero-padded so it's 4 digits wide
    - AA is the sequence number 
        (if the sequence number is one digit, the second character is ' ')
        (if there is no sequence number, the characters are '  ', except at the end of the string, in which case it's an empty string)
    - BB are any course numbering conventions, following the same rules specified in catalogparser.py 
        (if the course numbering convention is one digit, the second character is ' ')
        (if there are no course number conventions, the characters are '  ', except at the end of the string, in which case it's an empty string)
    - DEPT is the subject area code without spaces
    
    A may be a two digit code if and only if B is not a two digit code, and vice versa. The number of characters between XXXX and DEPT
    must always be 4.

    For example, the unencoded token for Computer Science M151B is
        0151B M COMSCI0151BM
    '''
    def get_token(self):
        if self.subj_area == '' or self.ctlg_no == '':
            raise ValueError
        else:
            unencoded_token = self._get_full_ctlg_no() + self._get_path()

            unencoded_bytes = unencoded_token.encode('utf-8')
            base64_token_bytes = base64.standard_b64encode(unencoded_bytes)
            return base64_token_bytes.decode('utf-8')

    def _get_padded_ctlg_no(self):
        return self.ctlg_no.zfill(4)

    def _get_padded_seq_no(self):
        padded_seq_no = ''
        if len(self.seq_no) == 0:
            padded_seq_no = '  '
        elif len(self.seq_no) == 1:
            padded_seq_no = self.seq_no + ' '
        elif len(self.seq_no) == 2:
            padded_seq_no = self.seq_no
        else:
            raise ValueError
        return padded_seq_no

    def _get_padded_conventions(self):
        padded_conventions = ''
        if self.is_concurrent and self.is_multi_listed:
            padded_conventions = 'CM'
        elif self.is_concurrent and not self.is_multi_listed:
            padded_conventions = 'C '
        elif not self.is_concurrent and self.is_multi_listed:
            padded_conventions = 'M '
        else:
            padded_conventions = '  '
        return padded_conventions

    def _get_unspaced_subj_area(self):
        return self.subj_area.replace(' ', '')

    def _get_full_ctlg_no(self):
        return self._get_padded_ctlg_no() + self._get_padded_seq_no() + self._get_padded_conventions()

    def _get_path(self):
        return self._get_unspaced_subj_area() + self._get_padded_ctlg_no() + self._get_padded_seq_no().strip() + self._get_padded_conventions().strip()

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)