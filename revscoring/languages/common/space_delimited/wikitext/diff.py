from ...datasources.meta import LowerCase, TokenFrequency
from ...datasources.wikitext import diff
from ...features.meta import ItemLength

# Datasources

word_tokens_added = diff.tokens_added_in_types(
    {"word"}
    name="wikitext.diff.word_tokens_added",
)
"""
Returns a list of all word-tokens added in this revision.
"""

word_tokens_removed = diff.tokens_removed_in_types(
    {"word"}
    name="wikitext.diff.word_tokens_removed",
)
"""
Returns a list of all word-tokens added in this revision.
"""

# Features

words_added = ItemLength(
    "wikitext.diff.words_added",
    word_tokens_added
)

words_removed = ItemLength(
    "wikitext.diff.words_removed",
    word_tokens_added
)
