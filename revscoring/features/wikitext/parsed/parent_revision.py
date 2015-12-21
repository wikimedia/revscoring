from ....datasources import parent_revision
from .parsed_revision import ParsedRevision

parent_revision = ParsedRevision("wikitext.parsed.parent_revision",
                                 parent_revision.text)
