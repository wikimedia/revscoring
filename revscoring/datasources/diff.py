from deltas import segment_matcher
from deltas.tokenizers import wikitext_split

from . import parent_revision, revision
from .datasource import Datasource
from .util import WORD_RE


def process_operations(parent_revision_text, revision_text):
    parent_revision_text = parent_revision_text or ''
    revision_text = revision_text or ''

    a = wikitext_split.tokenize(parent_revision_text)
    b = wikitext_split.tokenize(revision_text)

    return [op for op in segment_matcher.diff(a, b)], a, b

operations = Datasource("diff.operations", process_operations,
                        depends_on=[parent_revision.text, revision.text])
"""
Returns a tuple that describes a the difference between the parent revision text
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


def process_added_words(diff_added_segments):
    return [match.group(0) for segment in diff_added_segments
            for match in WORD_RE.finditer(segment)]

added_words = Datasource("diff.added_words", process_added_words,
                         depends_on=[added_segments])
"""
Returns a list of all word tokens added in this revision.
"""

def process_removed_words(diff_removed_segments):
    return [match.group(0) for segment in diff_removed_segments
            for match in WORD_RE.finditer(segment)]

removed_words = Datasource("diff.removed_words", process_removed_words,
                           depends_on=[removed_segments])
"""
Returns a list of all word tokens removed in this revision.
"""
