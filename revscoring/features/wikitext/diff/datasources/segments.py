from .....datasources import Datasource
from ..util import prefix
from .operations import operations


def process_segments_added(diff_operations):
    operations, a, b = diff_operations

    return ["".join(b[op.b1:op.b2])
            for op in operations
            if op.name == "insert"]

segments_added = Datasource(prefix + ".segments_added",
                            process_segments_added,
                            depends_on=[operations])
"""
Returns a list of all contiguous segments of tokens added in this revision.
"""


def process_segments_removed(revision_diff):
    operations, a, b = revision_diff

    return ["".join(a[op.a1:op.a2])
            for op in operations
            if op.name == "delete"]

segments_removed = Datasource(prefix + ".segments_removed",
                              process_segments_removed,
                              depends_on=[operations])
"""
Returns a list of all contiguous segments of tokens removed in this revision.
"""
