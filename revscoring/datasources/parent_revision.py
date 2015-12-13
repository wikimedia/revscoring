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
