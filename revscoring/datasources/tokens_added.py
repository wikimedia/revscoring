from collections import namedtuple

from .datasource import Datasource
from .revision_diff import revision_diff


def process(revision_diff):
    
    operations, a, b = revision_diff
    
    return [t for op in operations
            if op.name == "insert"
            for t in b[op.b1:op.b2]]

tokens_added = Datasource("tokens_added", process, depends_on=[revision_diff])
