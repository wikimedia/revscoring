from itertools import groupby

from . import datasources
from ....datasources.meta import mappers
from ...feature import Feature
from ...meta import aggregators
from .util import prefix

chars_added = aggregators.sum(
    mappers.map(len, datasources.segments_added),
    name=prefix + ".chars_added"
)
"""
A count of the number of characters added in this edit.
"""

chars_removed = aggregators.sum(
    mappers.map(len, datasources.segments_removed),
    name=prefix + ".chars_removed"
)
"""
A count of the number of characters removed in this edit.
"""

numeric_chars_added = aggregators.sum(
    mappers.map(len, datasources.numbers_added),
    name=prefix + ".numeric_chars_added"
)
"""
A count of the number of numeric characters added in this edit.
"""

numeric_chars_removed = aggregators.sum(
    mappers.map(len, datasources.numbers_removed),
    name=prefix + ".numeric_chars_removed"
)
"""
A count of the number of numeric characters removed in this edit.
"""


whitespace_chars_added = aggregators.sum(
    mappers.map(len, datasources.whitespaces_added),
    name=prefix + ".whitespace_chars_added"
)
"""
A count of the number of whitespace characters added in this edit.
"""

whitespace_chars_removed = aggregators.sum(
    mappers.map(len, datasources.whitespaces_removed),
    name=prefix + ".whitespace_chars_removed"
)
"""
A count of the number of whitespace characters removed in this edit.
"""

markup_chars_added = aggregators.sum(
    mappers.map(len, datasources.markups_added),
    name=prefix + ".markup_chars_added"
)
"""
A count of the number of markup characters added in this edit.
"""

markup_chars_removed = aggregators.sum(
    mappers.map(len, datasources.markups_removed),
    name=prefix + ".markup_chars_removed"
)
"""
A count of the number of markup characters removed in this edit.
"""

cjk_chars_added = aggregators.sum(
    mappers.map(len, datasources.cjks_added),
    name=prefix + ".cjk_chars_added"
)
"""
A count of the number of cjk characters added in this edit.
"""

cjk_chars_removed = aggregators.sum(
    mappers.map(len, datasources.cjks_removed),
    name=prefix + ".cjk_chars_removed"
)
"""
A count of the number of cjk characters removed in this edit.
"""

entity_chars_added = aggregators.sum(
    mappers.map(len, datasources.entities_added),
    name=prefix + ".entity_chars_added"
)
"""
A count of the number of entity characters added in this edit.
"""

entity_chars_removed = aggregators.sum(
    mappers.map(len, datasources.entities_removed),
    name=prefix + ".entity_chars_removed"
)
"""
A count of the number of entity characters removed in this edit.
"""

url_chars_added = aggregators.sum(
    mappers.map(len, datasources.urls_added),
    name=prefix + ".url_chars_added"
)
"""
A count of the number of url characters added in this edit.
"""

url_chars_removed = aggregators.sum(
    mappers.map(len, datasources.urls_removed),
    name=prefix + ".url_chars_removed"
)
"""
A count of the number of url characters removed in this edit.
"""

word_chars_added = aggregators.sum(
    mappers.map(len, datasources.words_added),
    name=prefix + ".word_chars_added"
)
"""
A count of the number of word characters added in this edit.
"""

word_chars_removed = aggregators.sum(
    mappers.map(len, datasources.words_removed),
    name=prefix + ".word_chars_removed"
)
"""
A count of the number of word characters removed in this edit.
"""

uppercase_word_chars_added = aggregators.sum(
    mappers.map(len, datasources.uppercase_words_added),
    name=prefix + ".uppercase_word_chars_added"
)
"""
A count of the number of UPPERCASE word characters added in this edit.
"""

uppercase_word_chars_removed = aggregators.sum(
    mappers.map(len, datasources.uppercase_words_removed),
    name=prefix + ".uppercase_word_chars_removed"
)
"""
A count of the number of UPPERCASE word characters removed in this edit.
"""

punctuation_chars_added = aggregators.sum(
    mappers.map(len, datasources.punctuations_added),
    name=prefix + ".punctuation_chars_added"
)
"""
A count of the number of punctuation characters added in this edit.
"""

punctuation_chars_removed = aggregators.sum(
    mappers.map(len, datasources.punctuations_removed),
    name=prefix + ".punctuation_chars_removed"
)
"""
A count of the number of punctuation characters removed in this edit.
"""

break_chars_added = aggregators.sum(
    mappers.map(len, datasources.breaks_added),
    name=prefix + ".break_chars_added"
)
"""
A count of the number of break characters added in this edit.
"""

break_chars_removed = aggregators.sum(
    mappers.map(len, datasources.breaks_removed),
    name=prefix + ".break_chars_removed"
)
"""
A count of the number of break characters removed in this edit.
"""


def process_uppercase_chars_added(diff_segments_added):
    return sum((not c.lower() == c)
               for segment in diff_segments_added
               for c in segment)

uppercase_chars_added = \
    Feature(prefix + ".uppercase_chars_added",
            process_uppercase_chars_added,
            returns=int, depends_on=[datasources.segments_added])
"""
A count of the number of uppercase characters added in this edit.
"""


def process_uppercase_chars_removed(diff_segments_removed):
    return sum((not c.lower() == c)
               for segment in diff_segments_removed
               for c in segment)

uppercase_chars_removed = \
    Feature(prefix + ".uppercase_chars_removed",
            process_uppercase_chars_removed,
            returns=int, depends_on=[datasources.segments_removed])
"""
A count of the number of uppercase characters removed in this edit.
"""


def process_longest_repeated_char_added(diff_segments_added):
    if len(diff_segments_added) > 0:
        return max(sum(1 for _ in group)
                   for segment in diff_segments_added
                   for _, group in groupby(segment.lower()))
    else:
        return 1

longest_repeated_char_added = \
    Feature(prefix + ".longest_repeated_char_added",
            process_longest_repeated_char_added,
            returns=int, depends_on=[datasources.segments_added])
"""
The length of the most repeated character added.
"""
