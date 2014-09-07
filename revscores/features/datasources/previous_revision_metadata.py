from collections import namedtuple

from mw import Timestamp

from ..dependencies import depends_on
from .previous_rev_doc import previous_rev_doc
from .revision_metadata import convert_doc, RevisionMetadata


@depends_on(previous_rev_doc)
def previous_revision_metadata(previous_rev_doc):
    return convert_doc(previous_rev_doc)
