"""
This features module provides access to features of the bytes of content in
revisions.

.. autodata:: revscoring.features.wikitext.revision

    Represents the base revision of interest.  Implements this a basic structure:

    * revision: :class:`~revscoring.features.wikitext.Revision`
        * parent: :class:`~revscoring.features.wikitext.Revision`
        * diff: :class:`~revscoring.features.wikitext.Diff`


Supporting classes
++++++++++++++++++
.. autoclass:: revscoring.features.wikitext.Revision
    :members:
    :inherited-members:
    :member-order: bysource

    :Character features:
        **chars** : `int`
            The number of characters
        **whitespace_chars** : `int`
            The number of whitespace characters
        **markup_chars** : `int`
            The number of wikitext markup characters
        **cjk_chars** : `int`
            The number of Chinese/Japanese/Korean characters
        **entity_chars** : `int`
            The number of HTML entity characters
        **url_chars** : `int`
            The number of URL characters
        **word_chars** : `int`
            The number of word characters
        **uppercase_word_chars** : `int`
            The number of UPPERCASE WORD characters
        **punctuation_chars** : `int`
            The number of punctuation characters
        **break_chars** : `int`
            The number of break characters
        **longest_repeated_char** : `int`
            The length of the most longest character repetition

    :Tokenized features:
        **tokens** : `int`
            The number of tokens
        **numbers** : `int`
            The number of number tokens
        **whitespaces** : `int`
            The number of whitespace tokens
        **markups** : `int`
            The number of markup tokens
        **cjks** : `int`
            The number of Chinese/Japanese/Korean tokens
        **entities** : `int`
            The number of HTML entity tokens
        **urls** : `int`
            The number of URL tokens
        **words** : `int`
            The number of word tokens
        **uppercase_words** : `int`
            The number of UPPERCASE word tokens
        **punctuations** : `int`
            The number of punctuation tokens
        **breaks** : `int`
            The number of break tokens
        **longest_token** : `int`
            The length of the longest token
        **longest_word** : `int`
            The length of the longest word-token

    :Parsed features:
        **content_chars** : `int`
            The number of characters of viewable content (no markup or
            templates)
        **headings** : `int`
            The number of headings
        **external_links** : `int`
            The number of external links
        **wikilinks** : `int`
            The number of wikilinks (internal to other pages in the wiki)
        **tags** : `int`
            The number of HTML tags
        **ref_tags** : `int`
            The number of <ref> tags
        **templates** : `int`
            The number of templates

.. autoclass:: revscoring.features.wikitext.Diff
    :members:
    :inherited-members:
    :member-order: bysource

    :Character features:
        **chars_added** : `int`
            The number of characters added
        **chars_removed** : `int`
            The number of characters removed
        **numeric_chars_added** : `int`
            The number of numeric characters added
        **numeric_chars_removed** : `int`
            The number of numeric characters removed
        **whitespace_chars_added** : `int`
            The number of whitespace characters added
        **whitespace_chars_removed** : `int`
            The number of whitespace characters removed
        **markup_chars_added** : `int`
            The number of markup characters added
        **markup_chars_removed** : `int`
            The number of markup characters removed
        **cjk_chars_added** : `int`
            The number of cjk characters added
        **cjk_chars_removed** : `int`
            The number of cjk characters removed
        **entity_chars_added** : `int`
            The number of entity characters added
        **entity_chars_removed** : `int`
            The number of entity characters removed
        **url_chars_added** : `int`
            The number of url characters added
        **url_chars_removed** : `int`
            The number of url characters removed
        **word_chars_added** : `int`
            The number of word characters added
        **word_chars_removed** : `int`
            The number of word characters removed
        **uppercase_word_chars_added** : `int`
            The number of UPPERCASE word characters added
        **uppercase_word_chars_removed** : `int`
            The number of UPPERCASE word characters removed
        **punctuation_chars_added** : `int`
            The number of punctuation characters added
        **punctuation_chars_removed** : `int`
            The number of punctuation characters removed
        **break_chars_added** : `int`
            The number of break characters added
        **break_chars_removed** : `int`
            The number of break characters removed
        **longest_repeated_char_added** : `int`
            The most repeated character added

    :Token frequency features:
        **token_delta_sum** : `int`
            The sum of delta changes in the token frequency table
        **token_delta_increase** : `int`
            The sum of delta increases in the token frequency table
        **token_delta_decrease** : `int`
            The sum of delta decreases in the token frequency table
        **token_prop_delta_sum** : `float`
            The sum of proportional delta changes in the token
            frequency table
        **token_prop_delta_increase** : `float`
            The sum of proportional delta increases in the token
            frequency table
        **token_prop_delta_decrease** : `float`
            The sum of proportional delta decreases in the token
            frequency table
        **number_delta_sum** : `int`
            The sum of delta changes in the number frequency table
        **number_delta_increase** : `int`
            The sum of delta increases in the number frequency table
        **number_delta_decrease** : `int`
            The sum of delta decreases in the number frequency table
        **number_prop_delta_sum** : `float`
            The sum of proportional delta changes in the number
            frequency table
        **number_prop_delta_increase** : `float`
            The sum of proportional delta increases in the number
            frequency table
        **number_prop_delta_decrease** : `float`
            The sum of proportional delta decreases in the number
            frequency table
        **whitespace_delta_sum** : `int`
            The sum of delta changes in the whitespace frequency table
        **whitespace_delta_increase** : `int`
            The sum of delta increases in the whitespace frequency table
        **whitespace_delta_decrease** : `int`
            The sum of delta decreases in the whitespace frequency table
        **whitespace_prop_delta_sum** : `float`
            The sum of proportional delta changes in the whitespace
            frequency table
        **whitespace_prop_delta_increase** : `float`
            The sum of proportional delta increases in the whitespace
            frequency table
        **whitespace_prop_delta_decrease** : `float`
            The sum of proportional delta decreases in the whitespace
            frequency table
        **markup_delta_sum** : `int`
            The sum of delta changes in the markup frequency table
        **markup_delta_increase** : `int`
            The sum of delta increases in the markup frequency table
        **markup_delta_decrease** : `int`
            The sum of delta decreases in the markup frequency table
        **markup_prop_delta_sum** : `float`
            The sum of proportional delta changes in the markup
            frequency table
        **markup_prop_delta_increase** : `float`
            The sum of proportional delta increases in the markup
            frequency table
        **markup_prop_delta_decrease** : `float`
            The sum of proportional delta decreases in the markup
            frequency table
        **cjk_delta_sum** : `int`
            The sum of delta changes in the cjk frequency table
        **cjk_delta_increase** : `int`
            The sum of delta increases in the cjk frequency table
        **cjk_delta_decrease** : `int`
            The sum of delta decreases in the cjk frequency table
        **cjk_prop_delta_sum** : `float`
            The sum of proportional delta changes in the cjk
            frequency table
        **cjk_prop_delta_increase** : `float`
            The sum of proportional delta increases in the cjk
            frequency table
        **cjk_prop_delta_decrease** : `float`
            The sum of proportional delta decreases in the cjk
            frequency table
        **entity_delta_sum** : `int`
            The sum of delta changes in the entity frequency table
        **entity_delta_increase** : `int`
            The sum of delta increases in the entity frequency table
        **entity_delta_decrease** : `int`
            The sum of delta decreases in the entity frequency table
        **entity_prop_delta_sum** : `float`
            The sum of proportional delta changes in the entity
            frequency table
        **entity_prop_delta_increase** : `float`
            The sum of proportional delta increases in the entity
            frequency table
        **entity_prop_delta_decrease** : `float`
            The sum of proportional delta decreases in the entity
            frequency table
        **url_delta_sum** : `int`
            The sum of delta changes in the url frequency table
        **url_delta_increase** : `int`
            The sum of delta increases in the url frequency table
        **url_delta_decrease** : `int`
            The sum of delta decreases in the url frequency table
        **url_prop_delta_sum** : `float`
            The sum of proportional delta changes in the url
            frequency table
        **url_prop_delta_increase** : `float`
            The sum of proportional delta increases in the url
            frequency table
        **url_prop_delta_decrease** : `float`
            The sum of proportional delta decreases in the url
            frequency table
        **word_delta_sum** : `int`
            The sum of delta changes in the word frequency table
        **word_delta_increase** : `int`
            The sum of delta increases in the word frequency table
        **word_delta_decrease** : `int`
            The sum of delta decreases in the word frequency table
        **word_prop_delta_sum** : `float`
            The sum of proportional delta changes in the word
            frequency table
        **word_prop_delta_increase** : `float`
            The sum of proportional delta increases in the word
            frequency table
        **word_prop_delta_decrease** : `float`
            The sum of proportional delta decreases in the word
            frequency table
        **uppercase_word_delta_sum** : `int`
            The sum of delta changes in the UPPERCASE word frequency
            table
        **uppercase_word_delta_increase** : `int`
            The sum of delta increases in the UPPERCASE word frequency
            table
        **uppercase_word_delta_decrease** : `int`
            The sum of delta decreases in the UPPERCASE word frequency
            table
        **uppercase_word_prop_delta_sum** : `float`
            The sum of proportional delta changes in the UPPERCASE word
            frequency table
        **uppercase_word_prop_delta_increase** : `float`
            The sum of proportional delta increases in the UPPERCASE word
            frequency table
        **uppercase_word_prop_delta_decrease** : `float`
            The sum of proportional delta decreases in the UPPERCASE word
            frequency table
        **punctuation_delta_sum** : `int`
            The sum of delta changes in the punctuation frequency table
        **punctuation_delta_increase** : `int`
            The sum of delta increases in the punctuation frequency table
        **punctuation_delta_decrease** : `int`
            The sum of delta decreases in the punctuation frequency table
        **punctuation_prop_delta_sum** : `float`
            The sum of proportional delta changes in the punctuation
            frequency table
        **punctuation_prop_delta_increase** : `float`
            The sum of proportional delta increases in the punctuation
            frequency table
        **punctuation_prop_delta_decrease** : `float`
            The sum of proportional delta decreases in the punctuation
            frequency table
        **break_delta_sum** : `int`
            The sum of delta changes in the break frequency table
        **break_delta_increase** : `int`
            The sum of delta increases in the break frequency table
        **break_delta_decrease** : `int`
            The sum of delta decreases in the break frequency table
        **break_prop_delta_sum** : `float`
            The sum of proportional delta changes in the break
            frequency table
        **break_prop_delta_increase** : `float`
            The sum of proportional delta increases in the break
            frequency table
        **break_prop_delta_decrease** : `float`
            The sum of proportional delta decreases in the break
            frequency table

    :Token edit features:
        **segments_added** : `int`
            The number of segments added
        **segments_removed** : `int`
            The number of segments removed
        **tokens_added** : `int`
            The number of tokens added
        **tokens_removed** : `int`
            The number of tokens removed
        **numbers_added** : `int`
            The number of number tokens added
        **numbers_removed** : `int`
            The number of number tokens removed
        **markups_added** : `int`
            The number of markup tokens added
        **markups_removed** : `int`
            The number of markup tokens removed
        **whitespaces_added** : `int`
            The number of whitespace tokens added
        **whitespaces_removed** : `int`
            The number of whitespace tokens removed
        **cjks_added** : `int`
            The number of cjk tokens added
        **cjks_removed** : `int`
            The number of cjk tokens removed
        **entities_added** : `int`
            The number of entity tokens added
        **entities_removed** : `int`
            The number of entity tokens removed
        **urls_added** : `int`
            The number of url tokens added
        **urls_removed** : `int`
            The number of url tokens removed
        **words_added** : `int`
            The number of word tokens added
        **words_removed** : `int`
            The number of word tokens removed
        **uppercase_words_added** : `int`
            The number of word tokens added
        **uppercase_words_removed** : `int`
            The number of word tokens removed
        **punctuations_added** : `int`
            The number of punctuation tokens added
        **punctuations_removed** : `int`
            The number of punctuation tokens removed
        **breaks_added** : `int`
            The number of break tokens added
        **breaks_removed** : `int`
            The number of break tokens removed
        **longest_token_added** : `int`
            The length of the longest token added"
        **longest_uppercase_word_added** : `int`
            The length of the longest sequence of UPPPERCASE characters
            added
"""  # noqa
from .revision_oriented import revision
from .features import Revision, Diff

__all__ = [revision, Revision, Diff]
