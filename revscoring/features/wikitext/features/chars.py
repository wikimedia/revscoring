from itertools import groupby

from ....datasources.meta import mappers
from ...feature import Feature
from ...meta import aggregators


class Revision:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.chars = aggregators.len(
            self.datasources.text,
            name=self.prefix + ".chars"
        )
        self.numeric_chars = aggregators.sum(
            mappers.map(len, self.datasources.numbers),
            name=self.prefix + ".numeric_chars", returns=int
        )
        self.whitespace_chars = aggregators.sum(
            mappers.map(len, self.datasources.whitespaces),
            name=self.prefix + ".whitespace_chars", returns=int
        )
        self.markup_chars = aggregators.sum(
            mappers.map(len, self.datasources.markups),
            name=self.prefix + ".markup_chars", returns=int
        )
        self.cjk_chars = aggregators.sum(
            mappers.map(len, self.datasources.cjks),
            name=self.prefix + ".cjk_chars", returns=int
        )
        self.entity_chars = aggregators.sum(
            mappers.map(len, self.datasources.entities),
            name=self.prefix + ".entity_chars", returns=int
        )
        self.url_chars = aggregators.sum(
            mappers.map(len, self.datasources.urls),
            name=self.prefix + ".url_chars", returns=int
        )
        self.word_chars = aggregators.sum(
            mappers.map(len, self.datasources.words),
            name=self.prefix + ".word_chars", returns=int
        )
        self.uppercase_word_chars = aggregators.sum(
            mappers.map(len, self.datasources.uppercase_words),
            name=self.prefix + ".uppercase_word_chars", returns=int
        )
        self.punctuation_chars = aggregators.sum(
            mappers.map(len, self.datasources.punctuations),
            name=self.prefix + ".punctuation_chars", returns=int
        )
        self.break_chars = aggregators.sum(
            mappers.map(len, self.datasources.breaks),
            name=self.prefix + ".break_chars", returns=int
        )


class Diff:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.chars_added = aggregators.sum(
            mappers.map(len, self.datasources.segments_added),
            name=self.prefix + ".chars_added", returns=int
        )
        """
        A count of the number of characters added in this edit.
        """

        self.chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.segments_removed),
            name=self.prefix + ".chars_removed", returns=int
        )
        """
        A count of the number of characters removed in this edit.
        """

        self.numeric_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.numbers_added),
            name=self.prefix + ".numeric_chars_added", returns=int
        )
        """
        A count of the number of numeric characters added in this edit.
        """

        self.numeric_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.numbers_removed),
            name=self.prefix + ".numeric_chars_removed", returns=int
        )
        """
        A count of the number of numeric characters removed in this edit.
        """

        self.whitespace_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.whitespaces_added),
            name=self.prefix + ".whitespace_chars_added", returns=int
        )
        """
        A count of the number of whitespace characters added in this edit.
        """

        self.whitespace_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.whitespaces_removed),
            name=self.prefix + ".whitespace_chars_removed", returns=int
        )
        """
        A count of the number of whitespace characters removed in this edit.
        """

        self.markup_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.markups_added),
            name=self.prefix + ".markup_chars_added", returns=int
        )
        """
        A count of the number of markup characters added in this edit.
        """

        self.markup_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.markups_removed),
            name=self.prefix + ".markup_chars_removed", returns=int
        )
        """
        A count of the number of markup characters removed in this edit.
        """

        self.cjk_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.cjks_added),
            name=self.prefix + ".cjk_chars_added", returns=int
        )
        """
        A count of the number of cjk characters added in this edit.
        """

        self.cjk_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.cjks_removed),
            name=self.prefix + ".cjk_chars_removed", returns=int
        )
        """
        A count of the number of cjk characters removed in this edit.
        """

        self.entity_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.entities_added),
            name=self.prefix + ".entity_chars_added", returns=int
        )
        """
        A count of the number of entity characters added in this edit.
        """

        self.entity_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.entities_removed),
            name=self.prefix + ".entity_chars_removed", returns=int
        )
        """
        A count of the number of entity characters removed in this edit.
        """

        self.url_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.urls_added),
            name=self.prefix + ".url_chars_added", returns=int
        )
        """
        A count of the number of url characters added in this edit.
        """

        self.url_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.urls_removed),
            name=self.prefix + ".url_chars_removed", returns=int
        )
        """
        A count of the number of url characters removed in this edit.
        """

        self.word_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.words_added),
            name=self.prefix + ".word_chars_added", returns=int
        )
        """
        A count of the number of word characters added in this edit.
        """

        self.word_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.words_removed),
            name=self.prefix + ".word_chars_removed", returns=int
        )
        """
        A count of the number of word characters removed in this edit.
        """

        self.uppercase_word_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.uppercase_words_added),
            name=self.prefix + ".uppercase_word_chars_added", returns=int
        )
        """
        A count of the number of UPPERCASE word characters added in this edit.
        """

        self.uppercase_word_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.uppercase_words_removed),
            name=self.prefix + ".uppercase_word_chars_removed", returns=int
        )
        """
        A count of the number of UPPERCASE word characters removed in this edit.
        """

        self.punctuation_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.punctuations_added),
            name=self.prefix + ".punctuation_chars_added", returns=int
        )
        """
        A count of the number of punctuation characters added in this edit.
        """

        self.punctuation_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.punctuations_removed),
            name=self.prefix + ".punctuation_chars_removed", returns=int
        )
        """
        A count of the number of punctuation characters removed in this edit.
        """

        self.break_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.breaks_added),
            name=self.prefix + ".break_chars_added", returns=int
        )
        """
        A count of the number of break characters added in this edit.
        """

        self.break_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.breaks_removed),
            name=self.prefix + ".break_chars_removed", returns=int
        )
        """
        A count of the number of break characters removed in this edit.
        """

        self.longest_repeated_char_added = \
            Feature(self.prefix + ".longest_repeated_char_added",
                    _process_longest_repeated_char_added,
                    returns=int, depends_on=[self.datasources.segments_added])
        """
        The length of the most repeated character added.
        """


def _process_longest_repeated_char_added(diff_segments_added):
    if len(diff_segments_added) > 0:
        return max(sum(1 for _ in group)
                   for segment in diff_segments_added
                   for _, group in groupby(segment.lower()))
    else:
        return 1
