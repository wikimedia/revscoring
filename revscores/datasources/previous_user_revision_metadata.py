from collections import namedtuple

from mw import Timestamp

from ..util.dependencies import depends
from .previous_user_rev_doc import previous_user_rev_doc
from .revision_metadata import convert_doc, RevisionMetadata


@depends(on=[previous_user_rev_doc])
def previous_user_revision_metadata(previous_user_rev_doc):
    return convert_doc(previous_user_rev_doc)
