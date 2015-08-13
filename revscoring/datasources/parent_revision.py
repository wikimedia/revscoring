from deltas.tokenizers import wikitext_split

from .datasource import Datasource

metadata = Datasource("parent_revision.metadata")
"""
Returns a :class:`~revscoring.datasources.types.RevisionMetadata` for the parent
revision.
"""

text = Datasource("parent_revision.text")
"""
Returns the text content of the parent revision.
"""

################################ Tokenized #####################################
def process_tokens(revision_text):
    return [t for t in wikitext_split.tokenize(revision_text or '')]

tokens = Datasource("revision.tokens",
                    process_tokens, depends_on=[text])
"""
Returns a list of tokens.
"""
