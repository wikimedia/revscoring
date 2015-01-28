from collections import namedtuple

from .datasource import Datasource
from .revision_diff import revision_diff


def process(revision_diff):
    
    operations, a, b = revision_diff
    
    return ["".join(a[op.a1:op.a2])
            for op in operations\
            if op.name == "delete"]

contiguous_segments_removed = Datasource("contiguous_segments_removed", process,
                                         depends_on=[revision_diff])
