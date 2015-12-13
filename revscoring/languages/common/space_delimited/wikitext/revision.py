from ...datasources.meta import LowerCase, TokenFrequency
from ...datasources.wikitext import revision
from ...features.meta import ItemLength

# Datasources
word_tokens = \
    revision.tokens_in_types({'words'},
                             name="wikitext.revision.word_tokens")
"""
Generates a list of word-tokens.
"""

content_word_tokens = revision.content_tokens_in_types(
    {'words'},
    name="wikitext.revision.content_word_tokens")
"""
Generates a list of word-tokens within content.
"""

lower_case_content_word_tokens = \
    LowerCase("wikitext.revision.lower_case_content_word_tokens"
              content_words)
"""
Generates a list of lower-cased content words-tokens.
"""

content_word_frequency = \
    TokenFrequency('wikitext.revision.content_word_frequency',
                   lower_case_content_words)
"""
Generates a `dict` of lower-cased content word frequency
"""

# Features
words = ItemLength("wikitext.revision.words", word_tokens)

content_words = ItemLength("wikitext.revision.content_words",
                           content_word_tokens)
