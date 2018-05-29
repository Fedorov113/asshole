class Archetype:
    def __init__(self):
        self.parent_archetype_id = ''
        self.archetype_id = '' #ARCHETYPE_HRID
        self.is_differential = False #Flag indicating whether this archetype is differential or flat in its contents. Top-level source archetypes have this flag set to True.
        self.definition = '' #C_COMPLEX_OBJECT 1
        self.terminology = '' #ARCHETYPE_TERMINOLOGY
        self.rules = [] #List<STATEMENT> 0..*

    def concept_code (self):
        return

    def physical_paths (self):
        return

    def logical_paths (self):
        return

    def specialisation_depth (self):
        return

    def is_specialised (self):
        return
