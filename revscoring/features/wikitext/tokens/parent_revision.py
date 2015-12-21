from ....datasources.parent_revision import text as parent_revision_text
from .tokenized_revision import TokenizedRevision

parent_revision = TokenizedRevision("tokens.parent_revision",
                                    parent_revision_text)
