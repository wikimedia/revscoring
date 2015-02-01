from collections import namedtuple

from .datasource import Datasource
from .revision_diff import revision_diff


def process(revision_diff):
    
    operations, a, b = revision_diff
    
    return ["".join(b[op.b1:op.b2])
            for op in operations\
            if op.name == "insert"]

contiguous_segments_added = Datasource("contiguous_segments_added", process,
                                       depends_on=[revision_diff])
