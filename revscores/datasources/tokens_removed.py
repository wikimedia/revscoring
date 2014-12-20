from collections import namedtuple

from .datasource import datasource_processor
from .revision_diff import revision_diff


@datasource_processor([revision_diff])
def tokens_removed(revision_diff):
    
    operations, a, b = revision_diff
    
    return [t for op in operations
            if op.name == "delete"
            for t in a[op.a1:op.a2]]
