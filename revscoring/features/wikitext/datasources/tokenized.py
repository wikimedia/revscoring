import re

from deltas import wikitext_split
from deltas.segmenters import ParagraphsSentencesAndWhitespace

from ....datasources import Datasource
from ....datasources.meta import filters, frequencies, mappers


class Revision:

    def __init__(self, name, revision_datasources):
        super().__init__(name, revision_datasources)

        self.tokens = tokenized(revision_datasources.text)
        """
        A list of all tokens
        """

        self.paragraphs_sentences_and_whitespace = Datasource(
            self._name + ".paragraphs_sentences_and_whitespace",
            paragraphs_sentences_and_whitespace.segment,
            depends_on=[self.tokens]
        )
        """
        A list of paragraphs, sentences, and whitespaces as segments.  See
        :class:`deltas.segmenters.Segment` and
        :class:`deltas.segmenters.MatchableSegment`.
        """

        self.token_frequency = frequencies.table(
            self.tokens,
            name=self._name + ".token_frequency"
        )
        """
        A frequency table of all tokens.
        """

        self.numbers = self.tokens_in_types(
            {'number'}, name=self._name + ".numbers"
        )
        """
        A list of numeric tokens
        """

        self.number_frequency = frequencies.table(
            self.numbers, name=self._name + ".number_frequency"
        )
        """
        A frequency table of number tokens.
        """

        self.whitespaces = self.tokens_in_types(
            {'whitespace'}, name=self._name + ".whitespaces"
        )
        """
        A list of whitespace tokens
        """

        self.whitespace_frequency = frequencies.table(
            self.whitespaces, name=self._name + ".whitespace_frequency"
        )
        """
        A frequency table of whichspace tokens.
        """

        self.markups = self.tokens_in_types(
            {'dbrack_open', 'dbrack_close', 'brack_open', 'brack_close',
             'tab_open', 'tab_close', 'dcurly_open', 'dcurly_close',
             'curly_open', 'curly_close', 'bold', 'italics', 'equals'},
            name=self._name + ".markups"
        )
        """
        A list of markup tokens
        """

        self.markup_frequency = frequencies.table(
            self.markups, name=self._name + ".markup_frequency"
        )
        """
        A frequency table of markup tokens.
        """

        self.cjks = self.tokens_in_types(
            {'cjk'}, name=self._name + ".cjks"
        )
        """
        A list of Chinese/Japanese/Korean tokens
        """

        self.cjk_frequency = frequencies.table(
            self.cjks, name=self._name + ".cjk_frequency"
        )
        """
        A frequency table of cjk tokens.
        """

        self.entities = self.tokens_in_types(
            {'entity'}, name=self._name + ".entities"
        )
        """
        A list of HTML entity tokens
        """

        self.entity_frequency = frequencies.table(
            self.entities, name=self._name + ".entity_frequency"
        )
        """
        A frequency table of entity tokens.
        """

        self.urls = self.tokens_in_types(
            {'url'}, name=self._name + ".urls"
        )
        """
        A list of URL tokens
        """

        self.url_frequency = frequencies.table(
            self.urls, name=self._name + ".url_frequency"
        )
        """
        A frequency table of url tokens.
        """

        self.words = self.tokens_in_types(
            {'word'}, name=self._name + ".words"
        )
        """
        A list of word tokens
        """

        self.word_frequency = frequencies.table(
            mappers.lower_case(self.words),
            name=self._name + ".word_frequency"
        )
        """
        A frequency table of lower-cased word tokens.
        """

        self.uppercase_words = filters.filter(
            is_uppercase_word, self.words,
            name=self._name + ".uppercase_words"
        )
        """
        A list of uppercase word tokens that are at least two
        characters long.
        """

        self.uppercase_word_frequency = frequencies.table(
            self.uppercase_words,
            name=self._name + ".uppercase_word_frequency"
        )
        """
        A frequency table of uppercase word tokens that are at least two
        characters long.
        """

        self.punctuations = self.tokens_in_types(
            {'period', 'qmark', 'epoint', 'comma', 'colon', 'scolon',
             'japan_punct'},
            name=self._name + ".punctuations"
        )
        """
        A list of punctuation tokens
        """

        self.punctuation_frequency = frequencies.table(
            self.punctuations, name=self._name + ".punctuation_frequency"
        )
        """
        A frequency table of punctuation tokens.
        """

        self.breaks = self.tokens_in_types(
            {'break'}, name=self._name + ".breaks"
        )
        """
        A list of break tokens
        """

        self.break_frequency = frequencies.table(
            self.breaks, name=self._name + ".break_frequency"
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
                   .format(self._name + ".tokens_in_types", types)

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
            name = "{0}({1})" \
                   .format(self._name + ".tokens_matching", regex.pattern)

        return filters.regex_matching(regex, self.tokens,
                                      name=name)


class Diff():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.token_delta = frequencies.delta(
            self.revision.parent.token_frequency,
            self.revision.token_frequency,
            name=self._name + ".token_delta"
        )
        """
        A token frequency delta table
        """

        self.token_prop_delta = frequencies.prop_delta(
            self.revision.parent.token_frequency,
            self.token_delta,
            name=self._name + ".token_prop_delta"
        )
        """
        A token proportional frequency delta table
        """

        self.number_delta = frequencies.delta(
            self.revision.parent.number_frequency,
            self.revision.number_frequency,
            name=self._name + ".number_delta"
        )
        """
        A number frequency delta table
        """

        self.number_prop_delta = frequencies.prop_delta(
            self.revision.parent.number_frequency,
            self.number_delta,
            name=self._name + ".number_prop_delta"
        )
        """
        A number proportional frequency delta table
        """

        self.whitespace_delta = frequencies.delta(
            self.revision.parent.whitespace_frequency,
            self.revision.whitespace_frequency,
            name=self._name + ".whitespace_delta"
        )
        """
        A whitespace frequency delta table
        """

        self.whitespace_prop_delta = frequencies.prop_delta(
            self.revision.parent.whitespace_frequency,
            self.whitespace_delta,
            name=self._name + ".whitespace_prop_delta"
        )
        """
        A whitespace proportional frequency delta table
        """

        self.markup_delta = frequencies.delta(
            self.revision.parent.markup_frequency,
            self.revision.markup_frequency,
            name=self._name + ".markup_delta"
        )
        """
        A markup frequency delta table
        """

        self.markup_prop_delta = frequencies.prop_delta(
            self.revision.parent.markup_frequency,
            self.markup_delta,
            name=self._name + ".markup_prop_delta"
        )
        """
        A markup proportional frequency delta table
        """

        self.cjk_delta = frequencies.delta(
            self.revision.parent.cjk_frequency,
            self.revision.cjk_frequency,
            name=self._name + ".cjk_delta"
        )
        """
        A cjk frequency delta table
        """

        self.cjk_prop_delta = frequencies.prop_delta(
            self.revision.parent.cjk_frequency,
            self.cjk_delta,
            name=self._name + ".cjk_prop_delta"
        )
        """
        A cjk proportional frequency delta table
        """

        self.entity_delta = frequencies.delta(
            self.revision.parent.entity_frequency,
            self.revision.entity_frequency,
            name=self._name + ".entity_delta"
        )
        """
        A entity frequency delta table
        """

        self.entity_prop_delta = frequencies.prop_delta(
            self.revision.parent.entity_frequency,
            self.entity_delta,
            name=self._name + ".entity_prop_delta"
        )
        """
        A entity proportional frequency delta table
        """

        self.url_delta = frequencies.delta(
            self.revision.parent.url_frequency,
            self.revision.url_frequency,
            name=self._name + ".url_delta"
        )
        """
        A url frequency delta table
        """

        self.url_prop_delta = frequencies.prop_delta(
            self.revision.parent.url_frequency,
            self.url_delta,
            name=self._name + ".url_prop_delta"
        )
        """
        A url proportional frequency delta table
        """

        self.word_delta = frequencies.delta(
            self.revision.parent.word_frequency,
            self.revision.word_frequency,
            name=self._name + ".word_delta"
        )
        """
        A lower-cased word frequency delta table
        """

        self.word_prop_delta = frequencies.prop_delta(
            self.revision.parent.word_frequency,
            self.word_delta,
            name=self._name + ".word_prop_delta"
        )
        """
        A lower-cased word proportional frequency delta table
        """

        self.uppercase_word_delta = frequencies.delta(
            self.revision.parent.uppercase_word_frequency,
            self.revision.uppercase_word_frequency,
            name=self._name + ".uppercase_word_delta"
        )
        """
        A uppercase word frequency delta table
        """

        self.uppercase_word_prop_delta = frequencies.prop_delta(
            self.revision.parent.uppercase_word_frequency,
            self.uppercase_word_delta,
            name=self._name + ".uppercase_word_prop_delta"
        )
        """
        A uppercase word proportional frequency delta table
        """

        self.punctuation_delta = frequencies.delta(
            self.revision.parent.punctuation_frequency,
            self.revision.punctuation_frequency,
            name=self._name + ".punctuation_delta"
        )
        """
        A punctuation frequency delta table
        """

        self.punctuation_prop_delta = frequencies.prop_delta(
            self.revision.parent.punctuation_frequency,
            self.punctuation_delta,
            name=self._name + ".punctuation_prop_delta"
        )
        """
        A punctuation proportional frequency delta table
        """

        self.break_delta = frequencies.delta(
            self.revision.parent.break_frequency,
            self.revision.break_frequency,
            name=self._name + ".break_delta"
        )
        """
        A break frequency delta table
        """

        self.break_prop_delta = frequencies.prop_delta(
            self.revision.parent.break_frequency,
            self.break_delta,
            name=self._name + ".break_prop_delta"
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


paragraphs_sentences_and_whitespace = ParagraphsSentencesAndWhitespace()
