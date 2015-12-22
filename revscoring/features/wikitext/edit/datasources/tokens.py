import logging
import re

from .....datasources import Datasource
from .....datasources.meta import filters
from ...tokenized import TokenIsInTypes, is_uppercase_word
from ..util import prefix
from .operations import operations

logger = logging.getLogger(__name__)


def process_tokens_added(diff_operations):
    operations, a, b = diff_operations
    return [t for op in operations
            if op.name == "insert"
            for t in b[op.b1:op.b2]]
tokens_added = Datasource(prefix + ".tokens_added", process_tokens_added,
                          depends_on=[operations])
"""
Constructs a :class:`revscoring.Datasource` that returns a list of all tokens a
dded in this revision.
"""


def process_tokens_removed(diff_operations):
    operations, a, b = diff_operations
    return [t for op in operations
            if op.name == "delete"
            for t in a[op.a1:op.a2]]
tokens_removed = Datasource(prefix + ".tokens_removed", process_tokens_removed,
                            depends_on=[operations])
"""
Constructs a :class:`revscoring.Datasource` that returns a list of all tokens
removed in this revision.
"""


def tokens_added_matching(regex, name=None, regex_flags=re.I):
    if not hasattr(regex, "pattern"):
        regex = re.compile(regex, regex_flags)
    if name is None:
        name = "{0}({1})".format(prefix + ".tokens_added_matching",
                                 regex.pattern)
    return filters.regex_matching(regex, tokens_added, name=name)
"""
Constructs a :class:`revscoring.Datasource` that represents tokens
added that match a regular expression.
"""


def tokens_removed_matching(regex, name=None, regex_flags=re.I):
    if not hasattr(regex, "pattern"):
        regex = re.compile(regex, regex_flags)

    if name is None:
        name = "{0}({1})" \
               .format("edit.revision.tokens_removed_matching",
                       regex.pattern)

    return filters.regex_matching(regex, tokens_removed, name=name)
"""
Constructs a :class:`revscoring.Datasource` that represents tokens
removed that match a regular expression.
"""


def tokens_added_in_types(types, name=None):
    types = set(types)
    if name is None:
        name = "{0}({1})".format(prefix + ".tokens_added_in_types", types)
    return filters.filter(TokenIsInTypes(types).filter, tokens_added,
                          name=name)
"""
Constructs a :class:`revscoring.Datasource` that represents tokens
added that are within a set of types.
"""


def tokens_removed_in_types(types, name=None):
    types = set(types)
    if name is None:
        name = "{0}({1})".format(prefix + ".tokens_removed_in_types", types)
    return filters.filter(TokenIsInTypes(types).filter, tokens_removed,
                          name=name)
"""
Constructs a :class:`revscoring.Datasource` that represents tokens
removed that are within a set of types.
"""

numbers_added = tokens_added_in_types(
    {'number'},
    name=prefix + ".numbers_added"
)
"""
A list of numeric tokens added in the edit
"""

numbers_removed = tokens_removed_in_types(
    {'number'},
    name=prefix + ".numbers_removed"
)
"""
A list of numeric tokens removed in the edit
"""

whitespaces_added = tokens_added_in_types(
    {'whitespace'},
    name=prefix + ".whitespaces_added"
)
"""
A list of whitespace tokens added in the edit
"""

whitespaces_removed = tokens_removed_in_types(
    {'whitespace'},
    name=prefix + ".whitespaces_removed"
)
"""
A list of whitespace tokens removed in the edit
"""

markups_added = tokens_added_in_types(
    {'dbrack_open', 'dbrack_close', 'brack_open', 'brack_close', 'tab_open',
     'tab_close', 'dcurly_open', 'dcurly_close', 'curly_open', 'curly_close',
     'bold', 'italics', 'equals'},
    name=prefix + ".markups_added"
)
"""
A list of markup tokens added in the edit
"""

markups_removed = tokens_removed_in_types(
    {'dbrack_open', 'dbrack_close', 'brack_open', 'brack_close', 'tab_open',
     'tab_close', 'dcurly_open', 'dcurly_close', 'curly_open', 'curly_close',
     'bold', 'italics', 'equals'},
    name=prefix + ".markups_removed"
)
"""
A list of markup tokens removed in the edit
"""

cjks_added = tokens_added_in_types(
    {'cjk'},
    name=prefix + ".cjks_added"
)
"""
A list of Chinese/Japanese/Korean tokens added in the edit
"""

cjks_removed = tokens_removed_in_types(
    {'cjk'},
    name=prefix + ".cjks_removed"
)
"""
A list of Chinese/Japanese/Korean tokens removed in the edit
"""

entities_added = tokens_added_in_types(
    {'entity'},
    name=prefix + ".entities_added"
)
"""
A list of HTML entity tokens added in the edit
"""

entities_removed = tokens_removed_in_types(
    {'entity'},
    name=prefix + ".entities_removed"
)
"""
A list of HTML entity tokens removed in the edit
"""

urls_added = tokens_added_in_types(
    {'url'},
    name=prefix + ".urls_added"
)
"""
A list of URL tokens rempved in the edit
"""

urls_removed = tokens_removed_in_types(
    {'url'},
    name=prefix + ".urls_removed"
)
"""
A list of URL tokens added in the edit
"""

words_added = tokens_added_in_types(
    {'word'},
    name=prefix + ".words_added"
)
"""
A list of word tokens added in the edit
"""

words_removed = tokens_removed_in_types(
    {'word'},
    name=prefix + ".words_removed"
)
"""
A list of word tokens removed in the edit
"""

uppercase_words_added = filters.filter(
    is_uppercase_word, words_added,
    name=prefix + ".uppercase_words_added"
)
"""
A list of fully UPPERCASE word tokens added in the edit
"""

uppercase_words_removed = filters.filter(
    is_uppercase_word, words_removed,
    name=prefix + ".uppercase_words_removed"
)
"""
A list of fully UPPERCASE word tokens removed in the edit
"""

punctuations_added = tokens_added_in_types(
    {'period', 'qmark', 'epoint', 'comma', 'colon', 'scolon', 'japan_punct'},
    name=prefix + ".punctuations_added"
)
"""
A list of punctuation tokens added in the edit
"""

punctuations_removed = tokens_removed_in_types(
    {'period', 'qmark', 'epoint', 'comma', 'colon', 'scolon', 'japan_punct'},
    name=prefix + ".punctuations_removed"
)
"""
A list of punctuation tokens removed in the edit
"""

breaks_added = tokens_added_in_types(
    {'break'},
    name=prefix + ".breaks_added"
)
"""
A list of break tokens added in the edit
"""

breaks_removed = tokens_removed_in_types(
    {'break'},
    name=prefix + ".breaks_removed"
)
"""
A list of break tokens removed in the edit
"""
