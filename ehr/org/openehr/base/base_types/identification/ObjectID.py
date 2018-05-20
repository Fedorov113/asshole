class ObjectID:

    def __init__(self, value):

        # If value is empty string
        if not value:
            # TODO EXCEPTIONS
            print('Object ID string is empty')
        else:
            self.value = value

    
