from ....datasources import revision
from .parsed_revision import ParsedRevision

parent_revision = ParsedRevision("wikitext.parsed.parent_revision",
                                 revision.text)
