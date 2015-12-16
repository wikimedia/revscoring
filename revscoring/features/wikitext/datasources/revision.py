import re

import mwparserfromhell as mwp
from deltas.tokenizers import wikitext_split

from ...errors import RevisionNotFound
from ..datasource import Datasource
from ..meta import filter, map, regex_matching
from ..revision import text


def process_tokens(text):
    if text is None:
        raise RevisionNotFound()
    return [t for t in wikitext_split.tokenize(text)]

tokens = Datasource("wikitext.revision.tokens",
                    process_tokens, depends_on=[text])
"""
Returns a list of tokens.
"""


def tokens_matching(regex, name=None, regex_flags=re.I):
    if not hasattr(regex, "pattern"):
        regex = re.compile(regex, regex_flags)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.revision.tokens_matching",
                       regex.pattern)

    return regex_matching(regex, tokens, name=name)
"""
Constructs a :class:`revscoring.Datasource` that returns all content tokens
that match a regular expression.
"""


def tokens_in_types(types, name=None):
    types = set(types)

    if name is None:
        name = "{0}({1})" \
               .format("wikitext.revision.tokens_in_types",
                       types)

    return filter(lambda t: t.type in types, tokens, name=name)
"""
Constructs a :class:`revscoring.Datasource` that returns all content tokens
that are within a set of types.
"""

number_tokens = tokens_in_types(
    {'number'},
    name="wikitext.revision.number_tokens"
)
"""
Returns a list of numeric tokens
"""

whitespace_tokens = tokens_in_types(
    {'whitespace'},
    name="wikitext.revision.whitespace_tokens"
)
"""
Returns a list of whitespace tokens
"""

markup_tokens = tokens_in_types(
    {'dbrack_open', 'dbrack_close', 'brack_open', 'brack_close', 'tab_open',
     'tab_close', 'dcurly_open', 'dcurly_close', 'curly_open', 'curly_close',
     'bold', 'italics', 'equals'},
    name="wikitext.revision.markup_tokens"
)
"""
Returns a list of markup tokens
"""

cjk_tokens = tokens_in_types(
    {'cjk'},
    name="wikitext.revision.cjk_tokens"
)
"""
Returns a list of Chinese/Japanese/Korean tokens
"""

entity_tokens = tokens_in_types(
    {'entity'},
    name="wikitext.revision.entity_tokens"
)
"""
Returns a list of HTML entity tokens
"""

url_tokens = tokens_in_types(
    {'url'},
    name="wikitext.revision.url_tokens"
)
"""
Returns a list of URL tokens
"""

word_tokens = tokens_in_types(
    {'word'},
    name="wikitext.revision.word_tokens"
)
"""
Returns a list of word tokens
"""

punctuation_tokens = tokens_in_types(
    {'period', 'qmark', 'epoint', 'comma', 'colon', 'scolon'},
    name="wikitext.revision.punctuation_tokens"
)
"""
Returns a list of punctuation tokens
"""

break_tokens = tokens_in_types(
    {'break'},
    name="wikitext.revision.break_tokens"
)
"""
Returns a list of break tokens
"""
