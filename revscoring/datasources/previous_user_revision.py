from . import revision
from .datasource import Datasource
from .types import RevisionMetadata


def process_metadata():
    raise NotImplementedError()

metadata = Datasource("previous_user_revision.metadata", process_metadata, depends_on=[])
