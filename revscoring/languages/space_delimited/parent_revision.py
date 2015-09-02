from ...datasources import parent_revision
from .revision import Revision


class ParentRevision(Revision):

    DATASOURCE_MODULE = parent_revision
    MODULE_NAME = "parent_revision"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
