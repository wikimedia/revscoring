from collections import namedtuple

from mw import Timestamp

from .datasource import Datasource
from .first_rev_doc import first_rev_doc
from .revision_metadata import convert_doc, RevisionMetadata


def process(first_rev_doc):
    return convert_doc(first_rev_doc)

first_revision_metadata = Datasource("first_revision_metadata", process,
                                     depends_on=[first_rev_doc])
