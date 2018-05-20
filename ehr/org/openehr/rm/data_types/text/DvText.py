from ..DataValue import DataValue

class DvText(DataValue):
    def __init__(self, value, hyperlink):
        super().__init__()

        self.value = value
        self.hyperlink = hyperlink
        self.formatting = ''
        self.language = ""
        self.encoding = ""