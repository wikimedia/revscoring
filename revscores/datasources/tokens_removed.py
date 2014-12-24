from collections import namedtuple

from .datasource import Datasource
from .revision_diff import revision_diff


def process(revision_diff):
    
    operations, a, b = revision_diff
    
    return [t for op in operations
            if op.name == "delete"
            for t in a[op.a1:op.a2]]

tokens_removed = Datasource("tokens_removed", process,
                            depends_on=[revision_diff])
