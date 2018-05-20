from ehr.org.openehr.am.aom2.definitions.AdlCodeDefinitions import AdlCodeDefinitions


class ArchetypeConstraint(AdlCodeDefinitions):
    """
    Abstract parent of all constraint model types. Defines conformance and congruence function signatures.
    """

    def __init__(self):
        super().__init__()
        self.parent = ArchetypeConstraint()
        self.soc_parent = None  # C_SEC_ORD

    # abstract
    def is_prohibited(self):
        return

    def has_path (self, a_path):
        return

    def path(self):
        return

    # abstract
    def c_conforms_to (self):
        return

    # abstract
    def c_congruent_to (self):
        return

    def is_second_order_constrained (self):
        return

    def is_root (self):
        return
    def is_leaf (self):
        return