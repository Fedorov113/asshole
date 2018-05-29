
class UID:

    def __init__(self, value):
        if not value:
            raise ValueError('UID value is empty')
        else:
            self.value = value