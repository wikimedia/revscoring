import logging
import re
import time

from deltas import segment_matcher

from . import parent_revision, revision
from ..datasource import Datasource
from ..meta import ItemFilter, TokensMatching

logger = logging.getLogger(__name__)


def process_operations(a, b):
    start = time.time()
    operations = [op for op in segment_matcher.diff(a, b)]
    logger.debug("diff() of {0} and {1} tokens took {2} seconds."
                 .format(len(a), len(b), time.time() - start))

    return operations, a, b

operations = Datasource("wikitext.diff.operations", process_operations,
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

tokens_added = Datasource("wikitext.diff.tokens_added", process_added_tokens,
                          depends_on=[operations])
"""
Returns a list of all tokens added in this revision.
"""


def tokens_added_matching(regex, name=None, regex_flags=re.I):
    if not hasattr(regex, "pattern"):
        regex = re.compile(regex, regex_flags)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.revision.tokens_added_matching",
                       regex.pattern)

    return TokensMatching(name, tokens_added, regex)
"""
Constructs a :class:`revscoring.Datasource` that returns all content tokens
added that match a regular expression.
"""


def tokens_added_in_types(types, name=None):
    types = set(types)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.diff.tokens_added_in_types",
                       types)

    return ItemFilter(name, tokens_added, lambda t: t.type in types)
"""
Constructs a :class:`revscoring.Datasource` that returns all content tokens
added that are within a set of types.
"""


def process_tokens_removed(diff_operations):

    operations, a, b = diff_operations

    return [t for op in operations
            if op.name == "delete"
            for t in a[op.a1:op.a2]]

tokens_removed = Datasource("wikitext.diff.tokens_removed",
                            process_tokens_removed,
                            depends_on=[operations])
"""
Returns a list of all tokens removed in this revision.
"""


def tokens_removed_matching(regex, name=None, regex_flags=re.I):
    if not hasattr(regex, "pattern"):
        regex = re.compile(regex, regex_flags)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.revision.tokens_removed_matching",
                       regex.pattern)

    return TokensMatching(name, tokens_removed, regex)
"""
Constructs a :class:`revscoring.Datasource` that returns all content tokens
removed that match a regular expression.
"""


def tokens_removed_in_types(types, name=None):
    types = set(types)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.diff.tokens_removed_in_types",
                       types)

    return ItemFilter(name, tokens_removed, lambda t: t.type in types)
"""
Constructs a :class:`revscoring.Datasource` that returns all content tokens
removed that are within a set of types.
"""


def process_segments_added(diff_operations):
    operations, a, b = diff_operations

    return ["".join(b[op.b1:op.b2])
            for op in operations
            if op.name == "insert"]

segments_added = Datasource("wikitext.diff.segments_added",
                            process_segments_added,
                            depends_on=[operations])
"""
Returns a list of all contiguous segments of tokens added in this revision.
"""


def process_segments_removed(revision_diff):
    operations, a, b = revision_diff

    return ["".join(a[op.a1:op.a2])
            for op in operations
            if op.name == "delete"]

segments_removed = Datasource("wikitext.diff.segments_removed",
                              process_segments_removed,
                              depends_on=[operations])
"""
Returns a list of all contiguous segments of tokens removed in this revision.
"""
