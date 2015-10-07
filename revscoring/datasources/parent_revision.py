import mwparserfromhell as mwp
from deltas.tokenizers import wikitext_split

from . import revision
from .datasource import Datasource

metadata = Datasource("parent_revision.metadata")
"""
Returns a :class:`~revscoring.datasources.types.RevisionMetadata` for the
parent revision.
"""

text = Datasource("parent_revision.text")
"""
Returns the text content of the parent revision.
"""


# ############################### Tokenized ###################################
def process_tokens(revision_text):
    return [t for t in wikitext_split.tokenize(revision_text or '')]

tokens = Datasource("parent_revision.tokens",
                    process_tokens, depends_on=[text])
"""
Returns a list of tokens.
"""


# ############################## Parse tree ###################################
def process_parse_tree(revision_text):
    return mwp.parse(revision_text or "")

parse_tree = Datasource("parent_revision.parse_tree",
                        process_parse_tree, depends_on=[text])
"""
Returns a :class:`mwparserfromhell.wikicode.Wikicode` abstract syntax tree
representing the content of the revision.
"""

content = Datasource("parent_revision.content", revision.process_content,
                     depends_on=[parse_tree])
"""
Returns the raw content (no markup or templates) of the revision.
"""

content_tokens = Datasource("parent_revision.content_tokens",
                            revision.process_content_tokens,
                            depends_on=[content])
"""
Returns tokens from the raw content (no markup or templates) of the current
revision
"""
