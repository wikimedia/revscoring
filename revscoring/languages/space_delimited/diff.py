from ...datasources import diff
from ...features import Feature
from ..meta.regex_extractors import SegmentRegexExtractor
from ..meta.token_filter import TokenFilter
from .util import WORD_RE


class Diff:

    def __init__(self, language):
        self.language = language
        self.prefix = language.__name__ + ".diff."

        self.added_words_list = TokenFilter(
            self.prefix + "words",
            diff.added_tokens,
            lambda t: t.type == "word"
        )
        """
        Returns a list of all word tokens added in this revision.
        """

        self.words_added = Feature(
            self.prefix + "words_added", len,
            returns=int,
            depends_on=[self.added_words_list]
        )
        """
        Returns a count of words added.
        """

        self.removed_words_list = TokenFilter(
            self.prefix + "words",
            diff.removed_tokens,
            lambda t: t.type == "word"
        )
        """
        Returns a list of all word tokens removed in this revision.
        """

        self.removed_words = Feature(
            self.prefix + "removed_words", len,
            returns=int,
            depends_on=[self.removed_words_list]
        )
        """
        Returns a count of words removed.
        """

        if language.resources.badwords:
            self.added_badwords_list = SegmentRegexExtractor(
                self.prefix + "added_badwords",
                diff.added_segments,
                language.resources.badwords
            )
            self.removed_badwords_list = SegmentRegexExtractor(
                self.prefix + "removed_badwords",
                diff.removed_segments,
                language.resources.badwords
            )

            self.badwords_added = Feature(
                self.prefix + "badwords_added", len,
                returns=int,
                depends_on=[self.added_badwords_list]
            )
            self.badwords_removed = Feature(
                self.prefix + "badwords_removed", len,
                returns=int,
                depends_on=[self.removed_badwords_list]
            )

        if language.resources.informals:
            self.added_informals_list = SegmentRegexExtractor(
                self.prefix + "added_informals",
                diff.added_segments,
                language.resources.informals
            )
            self.removed_informals_list = SegmentRegexExtractor(
                self.prefix + "removed_informals",
                diff.removed_segments,
                language.resources.informals
            )

            self.informals_added = Feature(
                self.prefix + "informals_added", len,
                returns=int,
                depends_on=[self.added_informals_list]
            )
            self.informals_removed = Feature(
                self.prefix + "informals_removed", len,
                returns=int,
                depends_on=[self.removed_informals_list]
            )

        if language.resources.dictionary:

            self.added_misspellings_list = TokenFilter(
                self.prefix + "added_misspellings",
                self.added_words_list,
                lambda w: not sd.resources.dictionary.check(w)
            )
            self.removed_misspellings_list = TokenFilter(
                self.prefix + "removed_misspellings",
                self.removed_words_list,
                lambda w: not sd.resources.dictionary.check(w)
            )

            self.misspellings_added = Feature(
                self.prefix + "misspellings_added", len,
                returns=int,
                depends_on=[self.added_misspellings_list]
            )
            self.misspellings_removed = Feature(
                self.prefix + "misspellings_removed", len,
                returns=int,
                depends_on=[self.removed_misspellings_list]
            )
