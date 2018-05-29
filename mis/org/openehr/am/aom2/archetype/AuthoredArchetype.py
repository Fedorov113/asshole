from .Archetype import Archetype
from mis.org.openehr.rm.common.resource.AuthoredResource import AuthoredResource

class AuthoredArchetype(Archetype, AuthoredResource):
    def __init__(self):
        super().__init__()

        self.adl_version = ''
        self.build_uid = '' #UUID
        self.rm_release = ''
        self.is_generated = ''
        self.other_meta_data = '' #Hash<String, String>
