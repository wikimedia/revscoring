from ...datasources import revision_oriented
from .parsed_revision import ParsedRevision

revision = ParsedRevision(
    "wikibase.revision",
    revision_oriented.revision.text,
    revision_oriented.revision.parent.text
)
