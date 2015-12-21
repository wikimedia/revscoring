from ....datasources.revision import text as revision_text
from .tokenized_revision import TokenizedRevision

revision = TokenizedRevision("tokens.revision", revision_text)
