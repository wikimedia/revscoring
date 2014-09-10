from collections import namedtuple

from ..util.dependencies import depends
from .revision_diff import revision_diff


@depends(on=[revision_diff])
def contiguous_segments_removed(revision_diff):
    
    operations, a, b = revision_diff
    
    return ["".join(a[op.a1:op.a2])
            for op in operations\
            if op.name == "delete"]
