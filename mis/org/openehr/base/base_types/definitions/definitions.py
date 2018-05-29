
class BasicDefinitions:
    """
    Defines globally used constant values.
    """
    def __init__(self):
        CR = '\015'
        LF = '\012'
        any_type=''
        regex_any_pattern='.*'
        default_encoding = 'UTF-8'

class OpenEHRDefinitions(BasicDefinitions):
    """
        Inheritance class to provide access to constants defined in other packages.

    """
    def __init__(self):
        super().__init__()
        self.local_terminology_id='local'