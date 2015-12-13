from ...datasources.meta import LowerCase, TokenFrequency
from ...datasources.wikitext import parent_revision

# Datasources
word_tokens = \
    parent_revision.tokens_in_types({'words'},
                                    name="wikitext.parent_revision.word_tokens")
"""
Generates a list of word-tokens.
"""

content_word_tokens = parent_revision.content_tokens_in_types(
    {'words'},
    name="wikitext.parent_revision.content_word_tokens")
"""
Generates a list of word-tokens within content.
"""

lower_case_content_word_tokens = \
    LowerCase("wikitext.parent_revision.lower_case_content_word_tokens"
              content_words)
"""
Generates a list of lower-cased content words-tokens.
"""

content_word_frequency = \
    TokenFrequency('wikitext.parent_revision.content_word_frequency',
                   lower_case_content_words)
"""
Generates a `dict` of lower-cased content word frequency
"""


# Features
words = ItemLength("wikitext.parent_revision.words", word_tokens)

content_words = ItemLength("wikitext.parent_revision.content_words",
                           content_word_tokens)
