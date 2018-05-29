from mis.org.openehr.rm.data_types.DataValue import DataValue

class DvBoolean(DataValue):
    def __init__(self, value):
        super().__init__()
        self.value = value