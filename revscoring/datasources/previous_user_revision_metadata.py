from collections import namedtuple

from mw import Timestamp

from .datasource import Datasource
from .previous_user_rev_doc import previous_user_rev_doc
from .revision_metadata import convert_doc, RevisionMetadata


def process(previous_user_rev_doc):
    return convert_doc(previous_user_rev_doc)

previous_user_revision_metadata = \
        Datasource("previous_user_revision_metadata", process,
                   depends_on=[previous_user_rev_doc])
