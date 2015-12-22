from ....datasources import revision_oriented
from .tokenized_revision import TokenizedRevision

revision = TokenizedRevision(
    "tokenized.revision",
    revision_oriented.revision.text,
    revision_oriented.revision.parent.text
)
