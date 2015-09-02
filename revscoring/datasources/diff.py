import logging
import time

from deltas import segment_matcher

from . import parent_revision, revision
from .datasource import Datasource

logger = logging.getLogger(__name__)


def process_operations(a, b):
    start = time.time()
    operations = [op for op in segment_matcher.diff(a, b)]
    logger.debug("diff() of {0} and {1} tokens took {2} seconds."
                 .format(len(a), len(b), time.time() - start))

    return operations, a, b

operations = Datasource("diff.operations", process_operations,
                        depends_on=[parent_revision.tokens, revision.tokens])
"""
Returns a tuple that describes the difference between the parent revision text
and the current revision's text.

The tuple contains three fields:

* operations: `list` of :class:`deltas.Operation`
* A tokens: `list` of `str`
* B tokens: `list` of `str`
"""


def process_added_tokens(diff_operations):

    operations, a, b = diff_operations

    return [t for op in operations
            if op.name == "insert"
            for t in b[op.b1:op.b2]]

added_tokens = Datasource("diff.added_tokens", process_added_tokens,
                          depends_on=[operations])
"""
Returns a list of all tokens added in this revision.
"""


def process_removed_tokens(diff_operations):

    operations, a, b = diff_operations

    return [t for op in operations
            if op.name == "delete"
            for t in a[op.a1:op.a2]]

removed_tokens = Datasource("removed_tokens", process_removed_tokens,
                            depends_on=[operations])
"""
Returns a list of all tokens removed in this revision.
"""


def process_added_segments(diff_operations):
    operations, a, b = diff_operations

    return ["".join(b[op.b1:op.b2])
            for op in operations
            if op.name == "insert"]

added_segments = Datasource("diff.added_segments", process_added_segments,
                            depends_on=[operations])
"""
Returns a list of all contiguous segments of tokens added in this revision.
"""


def process_removed_segments(revision_diff):
    operations, a, b = revision_diff

    return ["".join(a[op.a1:op.a2])
            for op in operations
            if op.name == "delete"]

removed_segments = Datasource("diff.removed_segments",
                              process_removed_segments,
                              depends_on=[operations])
"""
Returns a list of all contiguous segments of tokens removed in this revision.
"""
