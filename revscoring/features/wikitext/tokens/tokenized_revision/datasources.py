import re

from .....datasources.meta import filters, frequencies, mappers
from ....meta import aggregators
from ..tokenized import tokenized


class Datasources:

    def __init__(self, prefix, tokens_datasource):

        self.tokens = tokens_datasource
        """
        A list of all tokens
        """

        self.token_frequency = frequencies.table(
            self.tokens,
            name=prefix + ".token_frequency"
        )
        """
        A frequency table of all tokens.
        """

        self.numbers = self.tokens_in_types(
            {'number'},
            name=prefix + ".numbers"
        )
        """
        A list of numeric tokens
        """

        self.number_frequency = frequencies.table(
            self.numbers,
            name=prefix + ".number_frequency"
        )
        """
        A frequency table of number tokens.
        """

        self.whitespaces = self.tokens_in_types(
            {'whitespace'},
            name=prefix + ".whitespaces"
        )
        """
        A list of whitespace tokens
        """

        self.whitespace_frequency = frequencies.table(
            self.whitespaces,
            name=prefix + ".whitespace_frequency"
        )
        """
        A frequency table of whichspace tokens.
        """

        self.markups = self.tokens_in_types(
            {'dbrack_open', 'dbrack_close', 'brack_open', 'brack_close',
             'tab_open', 'tab_close', 'dcurly_open', 'dcurly_close',
             'curly_open', 'curly_close', 'bold', 'italics', 'equals'},
            name=prefix + ".markups"
        )
        """
        A list of markup tokens
        """

        self.markup_frequency = frequencies.table(
            self.markups,
            name=prefix + ".markup_frequency"
        )
        """
        A frequency table of markup tokens.
        """

        self.cjks = self.tokens_in_types(
            {'cjk'},
            name=prefix + ".cjks"
        )
        """
        A list of Chinese/Japanese/Korean tokens
        """

        self.cjk_frequency = frequencies.table(
            self.cjks,
            name=prefix + ".cjk_frequency"
        )
        """
        A frequency table of cjk tokens.
        """

        self.entities = self.tokens_in_types(
            {'entity'},
            name=prefix + ".entities"
        )
        """
        A list of HTML entity tokens
        """

        self.entity_frequency = frequencies.table(
            self.entities,
            name=prefix + ".entity_frequency"
        )
        """
        A frequency table of entity tokens.
        """

        self.urls = self.tokens_in_types(
            {'url'},
            name=prefix + ".urls"
        )
        """
        A list of URL tokens
        """

        self.url_frequency = frequencies.table(
            self.urls,
            name=prefix + ".url_frequency"
        )
        """
        A frequency table of url tokens.
        """

        self.words = self.tokens_in_types(
            {'word'},
            name=prefix + ".words"
        )
        """
        A list of word tokens
        """

        self.word_frequency = frequencies.table(
            mappers.lower_case(self.words),
            name=prefix + ".word_frequency"
        )
        """
        A frequency table of lower-cased word tokens.
        """

        self.uppercase_words = filters.filter(
            is_uppercase_word, self.words,
            name=prefix + ".uppercase_words"
        )
        """
        A list of uppercase word tokens that are at least two
        characters long.
        """

        self.uppercase_word_frequency = frequencies.table(
            self.uppercase_words,
            name=prefix + ".uppercase_word_frequency"
        )
        """
        A frequency table of uppercase word tokens that are at least two
        characters long.
        """

        self.punctuations = self.tokens_in_types(
            {'period', 'qmark', 'epoint', 'comma', 'colon', 'scolon',
             'japan_punct'},
            name=prefix + ".punctuations"
        )
        """
        A list of punctuation tokens
        """

        self.punctuation_frequency = frequencies.table(
            self.punctuations,
            name=prefix + ".punctuation_frequency"
        )
        """
        A frequency table of punctuation tokens.
        """

        self.breaks = self.tokens_in_types(
            {'break'},
            name=prefix + ".breaks"
        )
        """
        A list of break tokens
        """

        self.break_frequency = frequencies.table(
            self.breaks,
            name=prefix + ".break_frequency"
        )
        """
        A frequency table of break tokens.
        """

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
                              self.tokens, name=name)

    def tokens_matching(self, regex, name=None, regex_flags=re.I):
        """
        Constructs a :class:`revscoring.Datasource` that returns all content
        tokens that match a regular expression.
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, regex_flags)

        if name is None:
            name = "{0}({1})".format("tokens_matching", regex.pattern)

        return filters.regex_matching(regex, self.tokens,
                                      name=name)


def is_uppercase_word(word_token):
    return len(word_token) > 1 and \
           sum(c.lower() != c for c in word_token) == len(word_token)


class TokenIsInTypes:

    def __init__(self, types):
        self.types = set(types)

    def filter(self, token):
        return token.type in self.types
