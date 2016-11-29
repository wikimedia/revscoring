import logging
import re
import time

from deltas import segment_matcher

from ....datasources import Datasource
from ....datasources.meta import filters
from .tokenized import TokenIsInTypes, is_uppercase_word

logger = logging.getLogger(__name__)


class Diff:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.operations = Datasource(
            self._name + ".operations", _process_operations,
            depends_on=[
                self.revision.parent.paragraphs_sentences_and_whitespace,
                self.revision.paragraphs_sentences_and_whitespace,
                self.revision.parent.tokens,
                self.revision.tokens]
        )
        """
        Returns a tuple that describes the difference between the parent
        revision text and the current revision's text.

        The tuple contains three fields:

        * operations: `list` of :class:`deltas.Operation`
        * A tokens: `list` of `str`
        * B tokens: `list` of `str`
        """

        self.segments_added = Datasource(
            self._name + ".segments_added", _process_segments_added,
            depends_on=[self.operations]
        )
        """
        Returns a list of all contiguous segments of tokens added in this
        revision.
        """

        self.segments_removed = Datasource(
            self._name + ".segments_removed", _process_segments_removed,
            depends_on=[self.operations]
        )
        """
        Returns a list of all contiguous segments of tokens removed in this
        revision.
        """

        self.tokens_added = Datasource(
            self._name + ".tokens_added", _process_tokens_added,
            depends_on=[self.operations]
        )
        """
        Constructs a :class:`revscoring.Datasource` that returns a list of all
        tokens added in this revision.
        """

        self.tokens_removed = Datasource(
            self._name + ".tokens_removed", _process_tokens_removed,
            depends_on=[self.operations]
        )
        """
        Constructs a :class:`revscoring.Datasource` that returns a list of all
        tokens removed in this revision.
        """

        self.numbers_added = self.tokens_added_in_types(
            {'number'}, name=self._name + ".numbers_added"
        )
        """
        A list of numeric tokens added in the edit
        """

        self.numbers_removed = self.tokens_removed_in_types(
            {'number'}, name=self._name + ".numbers_removed"
        )
        """
        A list of numeric tokens removed in the edit
        """

        self.whitespaces_added = self.tokens_added_in_types(
            {'whitespace'}, name=self._name + ".whitespaces_added"
        )
        """
        A list of whitespace tokens added in the edit
        """

        self.whitespaces_removed = self.tokens_removed_in_types(
            {'whitespace'}, name=self._name + ".whitespaces_removed"
        )
        """
        A list of whitespace tokens removed in the edit
        """

        self.markups_added = self.tokens_added_in_types(
            {'dbrack_open', 'dbrack_close', 'brack_open', 'brack_close',
             'tab_open', 'tab_close', 'dcurly_open', 'dcurly_close',
             'curly_open', 'curly_close', 'bold', 'italics', 'equals'},
            name=self._name + ".markups_added"
        )
        """
        A list of markup tokens added in the edit
        """

        self.markups_removed = self.tokens_removed_in_types(
            {'dbrack_open', 'dbrack_close', 'brack_open', 'brack_close',
             'tab_open', 'tab_close', 'dcurly_open', 'dcurly_close',
             'curly_open', 'curly_close', 'bold', 'italics', 'equals'},
            name=self._name + ".markups_removed"
        )
        """
        A list of markup tokens removed in the edit
        """

        self.cjks_added = self.tokens_added_in_types(
            {'cjk'}, name=self._name + ".cjks_added"
        )
        """
        A list of Chinese/Japanese/Korean tokens added in the edit
        """

        self.cjks_removed = self.tokens_removed_in_types(
            {'cjk'}, name=self._name + ".cjks_removed"
        )
        """
        A list of Chinese/Japanese/Korean tokens removed in the edit
        """

        self.entities_added = self.tokens_added_in_types(
            {'entity'}, name=self._name + ".entities_added"
        )
        """
        A list of HTML entity tokens added in the edit
        """

        self.entities_removed = self.tokens_removed_in_types(
            {'entity'}, name=self._name + ".entities_removed"
        )
        """
        A list of HTML entity tokens removed in the edit
        """

        self.urls_added = self.tokens_added_in_types(
            {'url'}, name=self._name + ".urls_added"
        )
        """
        A list of URL tokens rempved in the edit
        """

        self.urls_removed = self.tokens_removed_in_types(
            {'url'}, name=self._name + ".urls_removed"
        )
        """
        A list of URL tokens added in the edit
        """

        self.words_added = self.tokens_added_in_types(
            {'word'}, name=self._name + ".words_added"
        )
        """
        A list of word tokens added in the edit
        """

        self.words_removed = self.tokens_removed_in_types(
            {'word'}, name=self._name + ".words_removed"
        )
        """
        A list of word tokens removed in the edit
        """

        self.uppercase_words_added = filters.filter(
            is_uppercase_word, self.words_added,
            name=self._name + ".uppercase_words_added"
        )
        """
        A list of fully UPPERCASE word tokens added in the edit
        """

        self.uppercase_words_removed = filters.filter(
            is_uppercase_word, self.words_removed,
            name=self._name + ".uppercase_words_removed"
        )
        """
        A list of fully UPPERCASE word tokens removed in the edit
        """

        self.punctuations_added = self.tokens_added_in_types(
            {'period', 'qmark', 'epoint', 'comma', 'colon', 'scolon',
             'japan_punct'},
            name=self._name + ".punctuations_added"
        )
        """
        A list of punctuation tokens added in the edit
        """

        self.punctuations_removed = self.tokens_removed_in_types(
            {'period', 'qmark', 'epoint', 'comma', 'colon', 'scolon',
             'japan_punct'},
            name=self._name + ".punctuations_removed"
        )
        """
        A list of punctuation tokens removed in the edit
        """

        self.breaks_added = self.tokens_added_in_types(
            {'break'},
            name=self._name + ".breaks_added"
        )
        """
        A list of break tokens added in the edit
        """

        self.breaks_removed = self.tokens_removed_in_types(
            {'break'},
            name=self._name + ".breaks_removed"
        )
        """
        A list of break tokens removed in the edit
        """

    def tokens_added_matching(self, regex, name=None, regex_flags=re.I):
        """
        Constructs a :class:`revscoring.Datasource` that represents tokens
        added that match a regular expression.
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, regex_flags)
        if name is None:
            name = "{0}({1})".format(self._name + ".tokens_added_matching",
                                     regex.pattern)
        return filters.regex_matching(regex, self.tokens_added, name=name)

    def tokens_removed_matching(self, regex, name=None, regex_flags=re.I):
        """
        Constructs a :class:`revscoring.Datasource` that represents tokens
        removed that match a regular expression.
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, regex_flags)
        if name is None:
            name = "{0}({1})" \
                   .format(self._name + ".tokens_removed_matching",
                           regex.pattern)

        return filters.regex_matching(regex, self.tokens_removed, name=name)

    def tokens_added_in_types(self, types, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that represents tokens
        added that are within a set of types.
        """
        types = set(types)
        if name is None:
            name = "{0}({1})".format(self._name + ".tokens_added_in_types",
                                     types)
        return filters.filter(TokenIsInTypes(types).filter, self.tokens_added,
                              name=name)

    def tokens_removed_in_types(self, types, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that represents tokens
        removed that are within a set of types.
        """
        types = set(types)
        if name is None:
            name = "{0}({1})".format(self._name + ".tokens_removed_in_types",
                                     types)
        return filters.filter(TokenIsInTypes(types).filter,
                              self.tokens_removed, name=name)


def _process_operations(a_segments, b_segments, a, b):
    start = time.time()
    operations = list(segment_matcher.diff_segments(a_segments, b_segments))
    logger.debug("diff() of {0} and {1} tokens took {2} seconds."
                 .format(len(a), len(b), time.time() - start))

    return operations, a, b


def _process_segments_added(diff_operations):
    operations, a, b = diff_operations

    return ["".join(b[op.b1:op.b2])
            for op in operations
            if op.name == "insert"]


def _process_segments_removed(revision_diff):
    operations, a, b = revision_diff

    return ["".join(a[op.a1:op.a2])
            for op in operations
            if op.name == "delete"]


def _process_tokens_removed(diff_operations):
    operations, a, b = diff_operations
    return [t for op in operations
            if op.name == "delete"
            for t in a[op.a1:op.a2]]


def _process_tokens_added(diff_operations):
    operations, a, b = diff_operations
    return [t for op in operations
            if op.name == "insert"
            for t in b[op.b1:op.b2]]
