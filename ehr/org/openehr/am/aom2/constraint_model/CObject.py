from .ArchetypeConstraint import ArchetypeConstraint

class CObject(ArchetypeConstraint):

    def __init__(self):
        super().__init__()
        self.rm_type_name = ''
        self.occurences = '' #Multiplicity interval?
        self.node_id = ''
        self.is_deprecated = False
