from collections import namedtuple

from ..util.dependencies import depends_on
from .revision_diff import revision_diff


@depends_on(revision_diff)
def contiguous_segments_added(revision_diff):
    
    operations, a, b = revision_diff
    
    return ["".join(b[op.b1:op.b2])
            for op in operations\
            if op.name == "insert"]
