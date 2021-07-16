from itertools import groupby

from revscoring.datasources.meta import mappers

from ...feature import Feature
from ...meta import aggregators


class Revision:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.chars = aggregators.len(
            self.datasources.text,
            name=self._name + ".chars"
        )
        "`int` : The number of characters in the text"
        self.numeric_chars = aggregators.sum(
            mappers.map(len, self.datasources.numbers),
            name=self._name + ".numeric_chars", returns=int
        )
        "`int` : The number of numeric characters in the text"
        self.whitespace_chars = aggregators.sum(
            mappers.map(len, self.datasources.whitespaces),
            name=self._name + ".whitespace_chars", returns=int
        )
        "`int` : The number of whitespace characters in the text"
        self.markup_chars = aggregators.sum(
            mappers.map(len, self.datasources.markups),
            name=self._name + ".markup_chars", returns=int
        )
        "`int` : The number of wikitext markup characters in the text"
        self.cjk_chars = aggregators.sum(
            mappers.map(len, self.datasources.cjks),
            name=self._name + ".cjk_chars", returns=int
        )
        "`int` : The number of Chinese/Japanese/Korean characters in the text"
        self.entity_chars = aggregators.sum(
            mappers.map(len, self.datasources.entities),
            name=self._name + ".entity_chars", returns=int
        )
        "`int` : The number of HTML entity characters in the text"
        self.url_chars = aggregators.sum(
            mappers.map(len, self.datasources.urls),
            name=self._name + ".url_chars", returns=int
        )
        "`int` : The number of URL characters in the text"
        self.word_chars = aggregators.sum(
            mappers.map(len, self.datasources.words),
            name=self._name + ".word_chars", returns=int
        )
        "`int` : The number of word characters in the text"
        self.uppercase_word_chars = aggregators.sum(
            mappers.map(len, self.datasources.uppercase_words),
            name=self._name + ".uppercase_word_chars", returns=int
        )
        "`int` : The number of UPPERCASE WORD characters in the text"
        self.punctuation_chars = aggregators.sum(
            mappers.map(len, self.datasources.punctuations),
            name=self._name + ".punctuation_chars", returns=int
        )
        "`int` : The number of punctuation characters in the text"
        self.break_chars = aggregators.sum(
            mappers.map(len, self.datasources.breaks),
            name=self._name + ".break_chars", returns=int
        )
        "`int` : The number of break characters in the text"

        self.longest_repeated_char = \
            Feature(self._name + ".longest_repeated_char",
                    _process_longest_repeated_char,
                    returns=int, depends_on=[self.datasources.text])
        "`int` : The most repeated character"


class Diff:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.chars_added = aggregators.sum(
            mappers.map(len, self.datasources.segments_added),
            name=self._name + ".chars_added", returns=int
        )
        "`int` : The number of characters added"

        self.chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.segments_removed),
            name=self._name + ".chars_removed", returns=int
        )
        "`int` : The number of characters removed"

        self.numeric_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.numbers_added),
            name=self._name + ".numeric_chars_added", returns=int
        )
        "`int` : The number of numeric characters added"

        self.numeric_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.numbers_removed),
            name=self._name + ".numeric_chars_removed", returns=int
        )
        "`int` : The number of numeric characters removed"

        self.whitespace_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.whitespaces_added),
            name=self._name + ".whitespace_chars_added", returns=int
        )
        "`int` : The number of whitespace characters added"

        self.whitespace_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.whitespaces_removed),
            name=self._name + ".whitespace_chars_removed", returns=int
        )
        "`int` : The number of whitespace characters removed"

        self.markup_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.markups_added),
            name=self._name + ".markup_chars_added", returns=int
        )
        "`int` : The number of markup characters added"

        self.markup_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.markups_removed),
            name=self._name + ".markup_chars_removed", returns=int
        )
        "`int` : The number of markup characters removed"

        self.cjk_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.cjks_added),
            name=self._name + ".cjk_chars_added", returns=int
        )
        "`int` : The number of cjk characters added"

        self.cjk_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.cjks_removed),
            name=self._name + ".cjk_chars_removed", returns=int
        )
        "`int` : The number of cjk characters removed"

        self.entity_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.entities_added),
            name=self._name + ".entity_chars_added", returns=int
        )
        "`int` : The number of entity characters added"

        self.entity_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.entities_removed),
            name=self._name + ".entity_chars_removed", returns=int
        )
        "`int` : The number of entity characters removed"

        self.url_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.urls_added),
            name=self._name + ".url_chars_added", returns=int
        )
        "`int` : The number of url characters added"

        self.url_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.urls_removed),
            name=self._name + ".url_chars_removed", returns=int
        )
        "`int` : The number of url characters removed"

        self.word_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.words_added),
            name=self._name + ".word_chars_added", returns=int
        )
        "`int` : The number of word characters added"

        self.word_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.words_removed),
            name=self._name + ".word_chars_removed", returns=int
        )
        "`int` : The number of word characters removed"

        self.uppercase_word_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.uppercase_words_added),
            name=self._name + ".uppercase_word_chars_added", returns=int
        )
        "`int` : The number of UPPERCASE word characters added"

        self.uppercase_word_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.uppercase_words_removed),
            name=self._name + ".uppercase_word_chars_removed", returns=int
        )
        "`int` : The number of UPPERCASE word characters removed"

        self.punctuation_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.punctuations_added),
            name=self._name + ".punctuation_chars_added", returns=int
        )
        "`int` : The number of punctuation characters added"

        self.punctuation_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.punctuations_removed),
            name=self._name + ".punctuation_chars_removed", returns=int
        )
        "`int` : The number of punctuation characters removed"

        self.break_chars_added = aggregators.sum(
            mappers.map(len, self.datasources.breaks_added),
            name=self._name + ".break_chars_added", returns=int
        )
        "`int` : The number of break characters added"

        self.break_chars_removed = aggregators.sum(
            mappers.map(len, self.datasources.breaks_removed),
            name=self._name + ".break_chars_removed", returns=int
        )
        "`int` : The number of break characters removed"

        self.longest_repeated_char_added = \
            Feature(self._name + ".longest_repeated_char_added",
                    _process_longest_repeated_char_added,
                    returns=int, depends_on=[self.datasources.segments_added])
        "`int` : The most repeated character added"


def _process_longest_repeated_char_added(diff_segments_added):
    if len(diff_segments_added) > 0:
        return max(sum(1 for _ in group)
                   for segment in diff_segments_added
                   for _, group in groupby(segment.lower()))
    else:
        return 1


def _process_longest_repeated_char(text):
    if len(text or "") > 0:
        return max(sum(1 for _ in group)
                   for _, group in groupby(text.lower()))
    else:
        return 1
