from .ObjectID import ObjectID


class ArchetypeID(ObjectID):
    """
        Identifier for archetypes.
        Ideally these would identify globally unique archetypes.
        Lexical form:
            rm_originator '-' rm_name '-' rm_entity '.' concept_name { '-' specialisation }* '.v' number.
        """

    AXIS_SEPARATOR = "."
    SECTION_SEPARATOR = "-"
    NAME_PATTERN = "[a-zA-Z][a-zA-Z0-9()_/%$#&]*"
    VERSION_PATTERN = "[a-zA-Z0-9]+"
    
    def __init__(self, value: "human readable identifier, must be validated and splitted"):
        # will throw an eception if None
        super().__init__(value)
        # Will fill all required fields or throw Execption
        self.read_value(value)

    def read_value(self, value):
        """
        Splits value into parts.
        :param value:
        :return:
        """

        self.qualified_rm_entity = ''
        self.domain_concept = ''
        self.rm_originator = ''
        self.rm_name = ''
        self.rm_entity = ''
        self.specialisation = ''
        self.version_id = ''


    def to_value(self, qualified_rm_entity, domain_concept,
                 rm_originator, rm_name, rm_entity, specialisation,
                 version_id):
        """
        Generates value string from fields
        """

        return
