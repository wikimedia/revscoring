from . import revision
from ..errors import RevisionDocumentNotFound
from .datasource import Datasource
from .types import RevisionMetadata


def process_doc():
    raise NotImplementedError()

doc = Datasource("page_creation.doc", process_doc)


def process_metadata():
    return NotImplementedError()

metadata = Datasource("page_creation.metadata", process_metadata)
