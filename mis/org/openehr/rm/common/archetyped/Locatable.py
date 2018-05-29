from .Pathable import Pathable

class Locatable(Pathable):

    def __init__(self, parent, name,
                 archetype_node_id: "used to build archetype paths. Always "
                                    "in the form of an at code, e.g. at0005",
                 uid,
                 links: 'List of links to other arch acenctors (ENTRY< SECTION< so on)',
                 archetype_details: "ARCHETYPED",
                 feeder_audit: "FEEDER AUDIT"):
        super().__init__(parent)

        self.name = name
        self.archetype_node_id = archetype_node_id
        self.uid = uid

    def concept(self):
        """
        Clinical concept of the archetype as a whole (= derived from the archetype_node_id' of the root node)
        :return:
        """
        return "TEXT"

    def is_archetype_root(self):
        """
        True if this node is the root of an archetyped structure.
        :return:
        """
        return False