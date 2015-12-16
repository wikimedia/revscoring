from . import datasources
from ....datasources.meta import mappers
from ...meta import aggregators
from .util import prefix

print(dir(datasources))

tokens_added = aggregators.len(
    datasources.tokens_added,
    name=prefix + ".tokens_added"
)
"""
A count of the tokens added in this edit.
"""

tokens_removed = aggregators.len(
    datasources.tokens_removed,
    name=prefix + ".tokens_removed"
)
"""
A count of the tokens removed in this edit.
"""

numbers_added = aggregators.len(
    datasources.numbers_added,
    name=prefix + ".numbers_added"
)
"""
A count of the number tokens added in this edit.
"""

numbers_removed = aggregators.len(
    datasources.numbers_removed,
    name=prefix + ".numbers_removed"
)
"""
A count of the number tokens removed in this edit.
"""

markups_added = aggregators.len(
    datasources.markups_added,
    name=prefix + ".markups_added"
)
"""
A count of the markup tokens added in this edit.
"""

markups_removed = aggregators.len(
    datasources.markups_removed,
    name=prefix + ".markups_removed"
)
"""
A count of the markup tokens removed in this edit.
"""

whitespaces_added = aggregators.len(
    datasources.whitespaces_added,
    name=prefix + ".whitespaces_added"
)
"""
A count of the whitespace tokens added in this edit.
"""

whitespaces_removed = aggregators.len(
    datasources.whitespaces_removed,
    name=prefix + ".whitespaces_removed"
)
"""
A count of the whitespace tokens removed in this edit.
"""

cjks_added = aggregators.len(
    datasources.cjks_added,
    name=prefix + ".cjks_added"
)
"""
A count of the cjk tokens added in this edit.
"""

cjks_removed = aggregators.len(
    datasources.cjks_removed,
    name=prefix + ".cjks_removed"
)
"""
A count of the cjk tokens removed in this edit.
"""

entities_added = aggregators.len(
    datasources.entities_added,
    name=prefix + ".entities_added"
)
"""
A count of the entity tokens added in this edit.
"""

entities_removed = aggregators.len(
    datasources.entities_removed,
    name=prefix + ".entities_removed"
)
"""
A count of the entity tokens removed in this edit.
"""

urls_added = aggregators.len(
    datasources.urls_added,
    name=prefix + ".urls_added"
)
"""
A count of the url tokens added in this edit.
"""

urls_removed = aggregators.len(
    datasources.urls_removed,
    name=prefix + ".urls_removed"
)
"""
A count of the url tokens removed in this edit.
"""

words_added = aggregators.len(
    datasources.words_added,
    name=prefix + ".words_added"
)
"""
A count of the word tokens added in this edit.
"""

words_removed = aggregators.len(
    datasources.words_removed,
    name=prefix + ".words_removed"
)
"""
A count of the word tokens removed in this edit.
"""

uppercase_words_added = aggregators.len(
    datasources.uppercase_words_added,
    name=prefix + ".words_added"
)
"""
A count of the word tokens added in this edit.
"""

uppercase_words_removed = aggregators.len(
    datasources.uppercase_words_removed,
    name=prefix + ".words_removed"
)
"""
A count of the word tokens removed in this edit.
"""

punctuations_added = aggregators.len(
    datasources.punctuations_added,
    name=prefix + ".punctuations_added"
)
"""
A count of the punctuation tokens added in this edit.
"""

punctuations_removed = aggregators.len(
    datasources.punctuations_removed,
    name=prefix + ".punctuations_removed"
)
"""
A count of the punctuation tokens removed in this edit.
"""

breaks_added = aggregators.len(
    datasources.breaks_added,
    name=prefix + ".breaks_added"
)
"""
A count of the break tokens added in this edit.
"""

breaks_removed = aggregators.len(
    datasources.breaks_removed,
    name=prefix + ".breaks_removed"
)
"""
A count of the break tokens removed in this edit.
"""

longest_token_added = aggregators.max(
    mappers.map(len, datasources.tokens_added),
    name=prefix + '.longest_token_added'
)
"""
The length of the longest token added in the edit
"""

longest_uppercase_word_added = aggregators.max(
    mappers.map(len, datasources.uppercase_words_added)
)
"""
The length of the longest sequence of UPPPERCASE characters added in the edit
"""
