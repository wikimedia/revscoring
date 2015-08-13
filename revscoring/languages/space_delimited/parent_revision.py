from ...datasources import parent_revision
from ..meta.regex_extractors import TextRegexExtractor
from .revision import Revision
from .util import WORD_RE


class ParentRevision(Revision):

    DATASOURCE_MODULE = parent_revision
    MODULE_NAME = "parent_revision"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
