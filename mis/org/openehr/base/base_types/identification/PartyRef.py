from.ObjectRef import ObjectRef

class PartyRef(ObjectRef):
    def __init__(self):
        TYPE_LIST = ['PERSON', 'ORGANISATION', 'GROUP', 'AGENT',
                     'ROLE', 'PARTY', 'ACTOR']