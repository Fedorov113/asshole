class AdlCodeDefinitions:
    """
    Definitions relating to the internal code system of archetypes.


    """
    def __init__(self):
        self.id_code_leader = "id"
        self.value_code_leader = "at"
        self.value_set_code_leader = "ac"
        self.specialisation_separator = "."
        self.code_regex_pattern = "(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*"
        self.root_code_regex_pattern = "^id1(\.1)*$"
        self.primitive_node_id = "id9999"


    def codes_conformant(self,a_child_code, a_parent_code):
        """
        True if a_child_code conforms to a_parent_code in the sense of specialisation,
        i.e. is a_child_code the same as or more specialised than a_parent_code.
        :param a_child_code:
        :param a_parent_code:
        :return:
        """
        return False

    def is_adl_code (self, a_code):
        return

    def is_id_code(self, a_code):
        return

    def is_value_code(self, a_code):
        return

    def is_value_set_code(self, a_code):
        return

    def is_redefined_code(self, a_code):
        return

    def code_exists_at_level(self, a_code, a_level):
        return
