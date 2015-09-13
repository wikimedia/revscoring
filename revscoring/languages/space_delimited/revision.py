from ...datasources import revision
from ...errors import RevisionNotFound
from ...features import Feature
from ..meta.infonoise import Infonoise
from ..meta.regex_extractors import TextRegexExtractor
from ..meta.token_filter import TokenFilter
from .util import token_is_word, utf16_cleanup


def raise_rnf():
    raise RevisionNotFound()


class Revision:
    """
    Implements a set of features based on the revision of interest.
    """

    DATASOURCE_MODULE = revision
    MODULE_NAME = "revision"

    def __init__(self, language, error_if_missing=False):
        self.language = language
        self.prefix = language.__name__ + "." + self.MODULE_NAME + "."

        self.words_list = TokenFilter(
            self.prefix + "words",
            self.DATASOURCE_MODULE.tokens,
            token_is_word,
            if_none=raise_rnf if error_if_missing else None
        )
        """
        Returns a list of word tokens.
        """

        self.words = Feature(
            self.prefix + "words", len,
            returns=int,
            depends_on=[self.words_list]
        )
        """
        A count of the number of words in the revision.
        """

        self.content_words_list = TokenFilter(
            self.prefix + "content_words",
            self.DATASOURCE_MODULE.content_tokens,
            token_is_word,
            if_none=raise_rnf if error_if_missing else None
        )
        """
        Returns a list of words that appear in the (non-markup) content of the
        revision.
        """

        self.content_words = Feature(
            self.prefix + "content_words", len,
            returns=int,
            depends_on=[self.content_words_list]
        )
        """
        A count of the number of words in the (non-markup) content of the
        revision.
        """

        if language.resources.stopwords is not None and \
           language.resources.stemmer is not None:
            self.infonoise = Infonoise(
                self.prefix + "infonoise",
                language.resources.stopwords,
                language.resources.stemmer.stem,
                self.content_words_list
            )
            """
            Returns a score measuring the proportion of text remaining after
            filtering markup and stopwords and stemming the remaining words.
            This feature is commonly used in quality prediction.
            """

        if language.resources.badwords is not None:
            self.badwords_list = TextRegexExtractor(
                self.prefix + "badwords",
                self.DATASOURCE_MODULE.text,
                language.resources.badwords,
                if_none=raise_rnf if error_if_missing else None
            )
            """
            Returns a list of the badwords that appear in the text.
            """

            self.badwords = Feature(
                self.prefix + "badwords", len,
                returns=int,
                depends_on=[self.badwords_list]
            )
            """
            Returns a count of the badwords that appear in the text.
            """

        if language.resources.informals is not None:
            self.informals_list = TextRegexExtractor(
                self.prefix + "informals",
                self.DATASOURCE_MODULE.text,
                language.resources.informals,
                if_none=raise_rnf if error_if_missing else None
            )
            """
            Returns a list of the informal words that appear in the text
            """

            self.informals = Feature(
                self.prefix + "informals", len,
                returns=int,
                depends_on=[self.informals_list]
            )
            """
            Returns a count of the informal words that appear in the text
            """

        if language.resources.dictionary is not None:
            self.misspellings_list = TokenFilter(
                self.prefix + "misspellings",
                self.words_list,
                self.not_in_dictionary
            )
            """
            Returns a list of the misspellings that appear in the text
            """

            self.misspellings = Feature(
                self.prefix + "misspellings", len,
                returns=int,
                depends_on=[self.misspellings_list]
            )
            """
            Returns a count of the misspellings that appear in the text
            """

    def in_dictionary(self, word):
        return self.language.resources.dictionary.check(utf16_cleanup(word))

    def not_in_dictionary(self, word):
        return not self.in_dictionary(word)
