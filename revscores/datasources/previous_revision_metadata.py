from collections import namedtuple

from mw import Timestamp

from .datasource import Datasource
from .previous_rev_doc import previous_rev_doc
from .revision_metadata import convert_doc


def process(previous_rev_doc):
    return convert_doc(previous_rev_doc)

previous_revision_metadata = Datasource("previous_revision_metadata", process,
                                        depends_on=[previous_rev_doc])
