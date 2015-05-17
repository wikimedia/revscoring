from . import revision
from ..errors import RevisionDocumentNotFound
from .datasource import Datasource
from .types import RevisionMetadata

metadata = Datasource("page_creation.metadata")
