from ....datasources.revision import text as revision_text
from ....datasources.parent_revision import text as parent_revision_text

from .tokenized import tokenized
from .tokens import Tokens, TokenIsInTypes, is_uppercase_word
from .delta import Delta

revision = Tokens("tokens.revision", revision_text)

parent_revision = Tokens("tokens.parent_revision", parent_revision_text)

delta = Delta("tokens.diff", parent_revision, revision)

__all__ = [tokenized, Tokens, TokenIsInTypes, is_uppercase_word,
           Delta, revision, parent_revision, delta]
