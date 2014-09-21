from collections import namedtuple

from ..util.dependencies import depends
from .revision_diff import revision_diff


@depends(on=[revision_diff])
def tokens_added(revision_diff):
    
    operations, a, b = revision_diff
    
    return [t for op in operations
            if op.name == "insert"
            for t in b[op.b1:op.b2]]
