from .ArchetypeConstraint import ArchetypeConstraint

class CAttribute(ArchetypeConstraint):
    """
    Abstract model of constraint on any kind of attribute in a class model.

    """
    def __init__(self):
        super().__init__()
        self.rm_attribute_name = ''
        self.existence = ''# mult int
        self.differential_path = ''
        self.cardinality = None
        self.is_multiple = False
        self.children = [CObject]