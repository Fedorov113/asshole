class Archetyped:
    """
    An instance of the class ARCHETYPED contains the relevant archetype
    identification information, allowing generating archetypes
    to be matched up with data instances.
    """
    def __init__(self, archetype_id):
        self.archetype_id = archetype_id
        self.template_id =''
        self.rm_version = ''