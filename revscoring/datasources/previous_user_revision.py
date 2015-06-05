from . import revision
from .datasource import Datasource
from .types import RevisionMetadata

metadata = Datasource("previous_user_revision.metadata")
"""
Returns a :class:`~revscoring.datasources.types.RevisionMetadata` for the
previous user revision.
"""
