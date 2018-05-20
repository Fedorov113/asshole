from ..DataValue import DataValue

class DvURI(DataValue):
    def __init__(self, value):
        super().__init__()

        self.value = value