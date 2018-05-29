from .AuthoredArchetype import AuthoredArchetype

class Template(AuthoredArchetype):
    def __init__(self):
        super().__init__()
        self.overlays = [] #TEMPLATE_OVERLAY