from collections import namedtuple

from mw import Timestamp

from .datasource import datasource_processor
from .first_rev_doc import first_rev_doc
from .revision_metadata import convert_doc, RevisionMetadata


@datasource_processor([first_rev_doc])
def first_revision_metadata(first_rev_doc):
    return convert_doc(first_rev_doc)
