import re

from ....datasources.meta import filters, frequencies, mappers
from ....util import NamedDict
from ...meta import aggregators
from .tokenized import tokenized


class Tokens:

    def __init__(self, prefix, text_datasource=None, tokens_datasource=None):

        if tokens_datasource is None:
            if text_datasource is None:
                raise TypeError("Either text or tokens must be specified.")

            tokens_datasource = tokenized(text_datasource)

        # Datasources
        self.datasources = NamedDict()

        self.datasources.tokens = tokens_datasource
        """
        A list of all tokens
        """

        self.datasources.token_frequency = frequencies.table(
            self.datasources.tokens,
            name=prefix + ".token_frequency"
        )
        """
        A frequency table of all tokens.
        """

        self.datasources.numbers = self.tokens_in_types(
            {'number'},
            name=prefix + ".numbers"
        )
        """
        A list of numeric tokens
        """

        self.datasources.number_frequency = frequencies.table(
            self.datasources.numbers,
            name=prefix + ".number_frequency"
        )
        """
        A frequency table of number tokens.
        """

        self.datasources.whitespaces = self.tokens_in_types(
            {'whitespace'},
            name=prefix + ".whitespaces"
        )
        """
        A list of whitespace tokens
        """

        self.datasources.whitespace_frequency = frequencies.table(
            self.datasources.whitespaces,
            name=prefix + ".whitespace_frequency"
        )
        """
        A frequency table of whichspace tokens.
        """

        self.datasources.markups = self.tokens_in_types(
            {'dbrack_open', 'dbrack_close', 'brack_open', 'brack_close',
             'tab_open', 'tab_close', 'dcurly_open', 'dcurly_close',
             'curly_open', 'curly_close', 'bold', 'italics', 'equals'},
            name=prefix + ".markups"
        )
        """
        A list of markup tokens
        """

        self.datasources.markup_frequency = frequencies.table(
            self.datasources.markups,
            name=prefix + ".markup_frequency"
        )
        """
        A frequency table of markup tokens.
        """

        self.datasources.cjks = self.tokens_in_types(
            {'cjk'},
            name=prefix + ".cjks"
        )
        """
        A list of Chinese/Japanese/Korean tokens
        """

        self.datasources.cjk_frequency = frequencies.table(
            self.datasources.cjks,
            name=prefix + ".cjk_frequency"
        )
        """
        A frequency table of cjk tokens.
        """

        self.datasources.entities = self.tokens_in_types(
            {'entity'},
            name=prefix + ".entities"
        )
        """
        A list of HTML entity tokens
        """

        self.datasources.entity_frequency = frequencies.table(
            self.datasources.entities,
            name=prefix + ".entity_frequency"
        )
        """
        A frequency table of entity tokens.
        """

        self.datasources.urls = self.tokens_in_types(
            {'url'},
            name=prefix + ".urls"
        )
        """
        A list of URL tokens
        """

        self.datasources.url_frequency = frequencies.table(
            self.datasources.urls,
            name=prefix + ".url_frequency"
        )
        """
        A frequency table of url tokens.
        """

        self.datasources.words = self.tokens_in_types(
            {'word'},
            name=prefix + ".words"
        )
        """
        A list of word tokens
        """

        self.datasources.word_frequency = frequencies.table(
            mappers.lower_case(self.datasources.words),
            name=prefix + ".word_frequency"
        )
        """
        A frequency table of lower-cased word tokens.
        """

        self.datasources.uppercase_words = filters.filter(
            is_uppercase_word, self.datasources.words,
            name=prefix + ".uppercase_words"
        )
        """
        A list of uppercase word tokens that are at least two
        characters long.
        """

        self.datasources.uppercase_word_frequency = frequencies.table(
            self.datasources.uppercase_words,
            name=prefix + ".uppercase_word_frequency"
        )
        """
        A frequency table of uppercase word tokens that are at least two
        characters long.
        """

        self.datasources.punctuations = self.tokens_in_types(
            {'period', 'qmark', 'epoint', 'comma', 'colon', 'scolon',
             'japan_punct'},
            name=prefix + ".punctuations"
        )
        """
        A list of punctuation tokens
        """

        self.datasources.punctuation_frequency = frequencies.table(
            self.datasources.punctuations,
            name=prefix + ".punctuation_frequency"
        )
        """
        A frequency table of punctuation tokens.
        """

        self.datasources.breaks = self.tokens_in_types(
            {'break'},
            name=prefix + ".breaks"
        )
        """
        A list of break tokens
        """

        self.datasources.break_frequency = frequencies.table(
            self.datasources.breaks,
            name=prefix + ".break_frequency"
        )
        """
        A frequency table of break tokens.
        """

        # Features

        self.tokens = aggregators.len(self.datasources.tokens)
        self.numbers = aggregators.len(self.datasources.numbers)
        self.whitespaces = aggregators.len(self.datasources.whitespaces)
        self.markups = aggregators.len(self.datasources.markups)
        self.cjks = aggregators.len(self.datasources.cjks)
        self.entities = aggregators.len(self.datasources.entities)
        self.urls = aggregators.len(self.datasources.urls)
        self.words = aggregators.len(self.datasources.words)
        self.uppercase_words = \
            aggregators.len(self.datasources.uppercase_words)
        self.punctuations = aggregators.len(self.datasources.punctuations)
        self.breaks = aggregators.len(self.datasources.breaks)

    def tokens_in_types(self, types, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that returns all content
        tokens that are within a set of types.
        """
        token_is_in_types = TokenIsInTypes(types)

        if name is None:
            name = "{0}({1})" \
                   .format("tokens_in_types", types)

        return filters.filter(token_is_in_types.filter,
                              self.datasources.tokens, name=name)

    def tokens_matching(self, regex, name=None, regex_flags=re.I):
        """
        Constructs a :class:`revscoring.Datasource` that returns all content
        tokens that match a regular expression.
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, regex_flags)

        if name is None:
            name = "{0}({1})".format("tokens_matching", regex.pattern)

        return filters.regex_matching(regex, self.datasources.tokens,
                                      name=name)


def is_uppercase_word(word_token):
    return len(word_token) > 1 and \
           sum(c.lower() != c for c in word_token) == len(word_token)


class TokenIsInTypes:

    def __init__(self, types):
        self.types = set(types)

    def filter(self, token):
        return token.type in self.types
