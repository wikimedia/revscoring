from ....datasources import revision_oriented
from .tokenized import tokenized
from .tokenized_revision import TokenizedRevision

revision = TokenizedRevision(
    "tokens.revision",
    tokenized(revision_oriented.revision.text),
    tokenized(revision_oriented.revision.parent.text)
)
