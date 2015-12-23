import re

from deltas import wikitext_split

from ....datasources import Datasource
from ....datasources.meta import filters, frequencies, mappers


class Revision():

    def __init__(self, prefix, revision_datasources):
        super().__init__(prefix, revision_datasources)

        self.tokens = tokenized(revision_datasources.text)
        """
        A list of all tokens
        """

        self.token_frequency = frequencies.table(
            self.tokens,
            name=self.prefix + ".token_frequency"
        )
        """
        A frequency table of all tokens.
        """

        self.numbers = self.tokens_in_types(
            {'number'}, name=self.prefix + ".numbers"
        )
        """
        A list of numeric tokens
        """

        self.number_frequency = frequencies.table(
            self.numbers, name=self.prefix + ".number_frequency"
        )
        """
        A frequency table of number tokens.
        """

        self.whitespaces = self.tokens_in_types(
            {'whitespace'}, name=self.prefix + ".whitespaces"
        )
        """
        A list of whitespace tokens
        """

        self.whitespace_frequency = frequencies.table(
            self.whitespaces, name=self.prefix + ".whitespace_frequency"
        )
        """
        A frequency table of whichspace tokens.
        """

        self.markups = self.tokens_in_types(
            {'dbrack_open', 'dbrack_close', 'brack_open', 'brack_close',
             'tab_open', 'tab_close', 'dcurly_open', 'dcurly_close',
             'curly_open', 'curly_close', 'bold', 'italics', 'equals'},
            name=self.prefix + ".markups"
        )
        """
        A list of markup tokens
        """

        self.markup_frequency = frequencies.table(
            self.markups, name=self.prefix + ".markup_frequency"
        )
        """
        A frequency table of markup tokens.
        """

        self.cjks = self.tokens_in_types(
            {'cjk'}, name=self.prefix + ".cjks"
        )
        """
        A list of Chinese/Japanese/Korean tokens
        """

        self.cjk_frequency = frequencies.table(
            self.cjks, name=self.prefix + ".cjk_frequency"
        )
        """
        A frequency table of cjk tokens.
        """

        self.entities = self.tokens_in_types(
            {'entity'}, name=self.prefix + ".entities"
        )
        """
        A list of HTML entity tokens
        """

        self.entity_frequency = frequencies.table(
            self.entities, name=self.prefix + ".entity_frequency"
        )
        """
        A frequency table of entity tokens.
        """

        self.urls = self.tokens_in_types(
            {'url'}, name=self.prefix + ".urls"
        )
        """
        A list of URL tokens
        """

        self.url_frequency = frequencies.table(
            self.urls, name=self.prefix + ".url_frequency"
        )
        """
        A frequency table of url tokens.
        """

        self.words = self.tokens_in_types(
            {'word'}, name=self.prefix + ".words"
        )
        """
        A list of word tokens
        """

        self.word_frequency = frequencies.table(
            mappers.lower_case(self.words),
            name=self.prefix + ".word_frequency"
        )
        """
        A frequency table of lower-cased word tokens.
        """

        self.uppercase_words = filters.filter(
            is_uppercase_word, self.words,
            name=self.prefix + ".uppercase_words"
        )
        """
        A list of uppercase word tokens that are at least two
        characters long.
        """

        self.uppercase_word_frequency = frequencies.table(
            self.uppercase_words,
            name=self.prefix + ".uppercase_word_frequency"
        )
        """
        A frequency table of uppercase word tokens that are at least two
        characters long.
        """

        self.punctuations = self.tokens_in_types(
            {'period', 'qmark', 'epoint', 'comma', 'colon', 'scolon',
             'japan_punct'},
            name=self.prefix + ".punctuations"
        )
        """
        A list of punctuation tokens
        """

        self.punctuation_frequency = frequencies.table(
            self.punctuations, name=self.prefix + ".punctuation_frequency"
        )
        """
        A frequency table of punctuation tokens.
        """

        self.breaks = self.tokens_in_types(
            {'break'}, name=self.prefix + ".breaks"
        )
        """
        A list of break tokens
        """

        self.break_frequency = frequencies.table(
            self.breaks, name=self.prefix + ".break_frequency"
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


class Diff():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.token_delta = frequencies.delta(
            self.revision.parent.token_frequency,
            self.revision.token_frequency,
            name=self.prefix + ".token_delta"
        )
        """
        A token frequency delta table
        """

        self.token_prop_delta = frequencies.prop_delta(
            self.revision.parent.token_frequency,
            self.token_delta,
            name=self.prefix + ".token_prop_delta"
        )
        """
        A token proportional frequency delta table
        """

        self.number_delta = frequencies.delta(
            self.revision.parent.number_frequency,
            self.revision.number_frequency,
            name=self.prefix + ".number_delta"
        )
        """
        A number frequency delta table
        """

        self.number_prop_delta = frequencies.prop_delta(
            self.revision.parent.number_frequency,
            self.number_delta,
            name=self.prefix + ".number_prop_delta"
        )
        """
        A number proportional frequency delta table
        """

        self.whitespace_delta = frequencies.delta(
            self.revision.parent.whitespace_frequency,
            self.revision.whitespace_frequency,
            name=self.prefix + ".whitespace_delta"
        )
        """
        A whitespace frequency delta table
        """

        self.whitespace_prop_delta = frequencies.prop_delta(
            self.revision.parent.whitespace_frequency,
            self.whitespace_delta,
            name=self.prefix + ".whitespace_prop_delta"
        )
        """
        A whitespace proportional frequency delta table
        """

        self.markup_delta = frequencies.delta(
            self.revision.parent.markup_frequency,
            self.revision.markup_frequency,
            name=self.prefix + ".markup_delta"
        )
        """
        A markup frequency delta table
        """

        self.markup_prop_delta = frequencies.prop_delta(
            self.revision.parent.markup_frequency,
            self.markup_delta,
            name=self.prefix + ".markup_prop_delta"
        )
        """
        A markup proportional frequency delta table
        """

        self.cjk_delta = frequencies.delta(
            self.revision.parent.cjk_frequency,
            self.revision.cjk_frequency,
            name=self.prefix + ".cjk_delta"
        )
        """
        A cjk frequency delta table
        """

        self.cjk_prop_delta = frequencies.prop_delta(
            self.revision.parent.cjk_frequency,
            self.cjk_delta,
            name=self.prefix + ".cjk_prop_delta"
        )
        """
        A cjk proportional frequency delta table
        """

        self.entity_delta = frequencies.delta(
            self.revision.parent.entity_frequency,
            self.revision.entity_frequency,
            name=self.prefix + ".entity_delta"
        )
        """
        A entity frequency delta table
        """

        self.entity_prop_delta = frequencies.prop_delta(
            self.revision.parent.entity_frequency,
            self.entity_delta,
            name=self.prefix + ".entity_prop_delta"
        )
        """
        A entity proportional frequency delta table
        """

        self.url_delta = frequencies.delta(
            self.revision.parent.url_frequency,
            self.revision.url_frequency,
            name=self.prefix + ".url_delta"
        )
        """
        A url frequency delta table
        """

        self.url_prop_delta = frequencies.prop_delta(
            self.revision.parent.url_frequency,
            self.url_delta,
            name=self.prefix + ".url_prop_delta"
        )
        """
        A url proportional frequency delta table
        """

        self.word_delta = frequencies.delta(
            self.revision.parent.word_frequency,
            self.revision.word_frequency,
            name=self.prefix + ".word_delta"
        )
        """
        A lower-cased word frequency delta table
        """

        self.word_prop_delta = frequencies.prop_delta(
            self.revision.parent.word_frequency,
            self.word_delta,
            name=self.prefix + ".word_prop_delta"
        )
        """
        A lower-cased word proportional frequency delta table
        """

        self.uppercase_word_delta = frequencies.delta(
            self.revision.parent.uppercase_word_frequency,
            self.revision.uppercase_word_frequency,
            name=self.prefix + ".uppercase_word_delta"
        )
        """
        A uppercase word frequency delta table
        """

        self.uppercase_word_prop_delta = frequencies.prop_delta(
            self.revision.parent.uppercase_word_frequency,
            self.uppercase_word_delta,
            name=self.prefix + ".uppercase_word_prop_delta"
        )
        """
        A uppercase word proportional frequency delta table
        """

        self.punctuation_delta = frequencies.delta(
            self.revision.parent.punctuation_frequency,
            self.revision.punctuation_frequency,
            name=self.prefix + ".punctuation_delta"
        )
        """
        A punctuation frequency delta table
        """

        self.punctuation_prop_delta = frequencies.prop_delta(
            self.revision.parent.punctuation_frequency,
            self.punctuation_delta,
            name=self.prefix + ".punctuation_prop_delta"
        )
        """
        A punctuation proportional frequency delta table
        """

        self.break_delta = frequencies.delta(
            self.revision.parent.break_frequency,
            self.revision.break_frequency,
            name=self.prefix + ".break_delta"
        )
        """
        A break frequency delta table
        """

        self.break_prop_delta = frequencies.prop_delta(
            self.revision.parent.break_frequency,
            self.break_delta,
            name=self.prefix + ".break_prop_delta"
        )
        """
        A break proportional frequency delta table
        """


def is_uppercase_word(word_token):
    return len(word_token) > 1 and \
           sum(c.lower() != c for c in word_token) == len(word_token)


class TokenIsInTypes:

    def __init__(self, types):
        self.types = set(types)

    def filter(self, token):
        return token.type in self.types


def _process_tokens(text):
    return [t for t in wikitext_split.tokenize(text or "")]


def tokenized(text_datasource, name=None):
    """
    Constructs a :class:`revision.Datasource` that generates a list of tokens
    """
    if name is None:
        name = "{0}({1})".format("tokenized", text_datasource)

    return Datasource(
        name, _process_tokens, depends_on=[text_datasource]
    )
