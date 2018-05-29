from .CDefinedObject import CDefinedObject

class CComplexObject(CDefinedObject):
    def __init__(self):
        super().__init__()
        self.attribute_tuples = ''