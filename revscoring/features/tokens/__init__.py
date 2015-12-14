from ..datasources import revision, parent_revision

from .tokenize import tokenize
from .tokens import Tokens
from .diff import Diff

revision_tokens = tokenize(revision.text, name="tokens.revision.tokens")
revision = Tokens("tokens.revision", revision_tokens)

parent_revision_tokens = tokenize(parent_revision.text,
                                  name="tokens.parent_revision.tokens")
parent_revision = Tokens("tokens.parent_revision", parent_revision_tokens)

diff = Diff(revision, parent_revision)
