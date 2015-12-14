import logging
import re
import time

from deltas import segment_matcher

from . import parent_revision, revision
from ..datasource import Datasource
from ..meta import filter, regex_matching

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

    return regex_matching(regex, tokens_added, name=name)
"""
Constructs a :class:`revscoring.Datasource` that returns all tokens
added that match a regular expression.
"""


def tokens_added_in_types(types, name=None):
    types = set(types)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.diff.tokens_added_in_types",
                       types)

    return filter(lambda t: t.type in types, tokens_added, name=name)
"""
Constructs a :class:`revscoring.Datasource` that returns all tokens
added that are within a set of types.
"""


number_tokens_added = tokens_added_in_types(
    {'number'},
    name="wikitext.diff.parent_revision.number_tokens_added"
)
"""
Returns a list of numeric tokens
"""

whitespace_tokens_added = tokens_added_in_types(
    {'whitespace'},
    name="wikitext.diff.parent_revision.whitespace_tokens_added"
)
"""
Returns a list of whitespace tokens
"""

markup_tokens_added = tokens_added_in_types(
    {'dbrack_open', 'dbrack_close', 'brack_open', 'brack_close', 'tab_open',
     'tab_close', 'dcurly_open', 'dcurly_close', 'curly_open', 'curly_close',
     'bold', 'italics', 'equals'},
    name="wikitext.diff.parent_revision.markup_tokens_added"
)
"""
Returns a list of markup tokens
"""

cjk_tokens_added = tokens_added_in_types(
    {'cjk'},
    name="wikitext.diff.parent_revision.cjk_tokens_added"
)
"""
Returns a list of Chinese/Japanese/Korean tokens
"""

entity_tokens_added = tokens_added_in_types(
    {'entity'},
    name="wikitext.diff.parent_revision.entity_tokens_added"
)
"""
Returns a list of HTML entity tokens
"""

url_tokens_added = tokens_added_in_types(
    {'url'},
    name="wikitext.diff.parent_revision.url_tokens_added"
)
"""
Returns a list of URL tokens
"""

word_tokens_added = tokens_added_in_types(
    {'word'},
    name="wikitext.diff.parent_revision.word_tokens_added"
)
"""
Returns a list of word tokens
"""

punctuation_tokens_added = tokens_added_in_types(
    {'period', 'qmark', 'epoint', 'comma', 'colon', 'scolon'},
    name="wikitext.diff.parent_revision.punctuation_tokens_added"
)
"""
Returns a list of punctuation tokens
"""

break_tokens_added = tokens_added_in_types(
    {'break'},
    name="wikitext.diff.parent_revision.break_tokens_added"
)
"""
Returns a list of break tokens
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

    return regex_matching(regex, tokens_removed, name=name)
"""
Constructs a :class:`revscoring.Datasource` that returns all tokens
removed that match a regular expression.
"""


def tokens_removed_in_types(types, name=None):
    types = set(types)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.diff.tokens_removed_in_types",
                       types)

    return filter(lambda t: t.type in types, tokens_removed, name=name)
"""
Constructs a :class:`revscoring.Datasource` that returns all tokens
removed that are within a set of types.
"""


number_tokens_removed = tokens_removed_in_types(
    {'number'},
    name="wikitext.diff.parent_revision.number_tokens_removed"
)
"""
Returns a list of numeric tokens
"""

whitespace_tokens_removed = tokens_removed_in_types(
    {'whitespace'},
    name="wikitext.diff.parent_revision.whitespace_tokens_removed"
)
"""
Returns a list of whitespace tokens
"""

markup_tokens_removed = tokens_removed_in_types(
    {'dbrack_open', 'dbrack_close', 'brack_open', 'brack_close', 'tab_open',
     'tab_close', 'dcurly_open', 'dcurly_close', 'curly_open', 'curly_close',
     'bold', 'italics', 'equals'},
    name="wikitext.diff.parent_revision.markup_tokens_removed"
)
"""
Returns a list of markup tokens
"""

cjk_tokens_removed = tokens_removed_in_types(
    {'cjk'},
    name="wikitext.diff.parent_revision.cjk_tokens_removed"
)
"""
Returns a list of Chinese/Japanese/Korean tokens
"""

entity_tokens_removed = tokens_removed_in_types(
    {'entity'},
    name="wikitext.diff.parent_revision.entity_tokens_removed"
)
"""
Returns a list of HTML entity tokens
"""

url_tokens_removed = tokens_removed_in_types(
    {'url'},
    name="wikitext.diff.parent_revision.url_tokens_removed"
)
"""
Returns a list of URL tokens
"""

word_tokens_removed = tokens_removed_in_types(
    {'word'},
    name="wikitext.diff.parent_revision.word_tokens_removed"
)
"""
Returns a list of word tokens
"""

punctuation_tokens_removed = tokens_removed_in_types(
    {'period', 'qmark', 'epoint', 'comma', 'colon', 'scolon'},
    name="wikitext.diff.parent_revision.punctuation_tokens_removed"
)
"""
Returns a list of punctuation tokens
"""

break_tokens_removed = tokens_removed_in_types(
    {'break'},
    name="wikitext.diff.parent_revision.break_tokens_removed"
)
"""
Returns a list of break tokens
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
