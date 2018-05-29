from .AuthoredArchetype import AuthoredArchetype

class OperationalTemplate(AuthoredArchetype):
    def __init__(self):
        super().__init__()
        self.component_terminologies = [] #Hash<String, ARCHETYPE_TERMINOLOGY>
        self.terminology_extracts = [] # Hash<String, ARCHETYPE_TERMINOLOGY>