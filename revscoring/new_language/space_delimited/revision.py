from ...datasources import revision
from ...errors import RevisionDocumentNotFound
from ...features import Feature
from ..meta.infonoise import Infonoise
from ..meta.regex_extractors import TextRegexExtractor
from ..meta.token_filter import TokenFilter
from .util import WORD_RE


def raise_rnf():
    raise RevisionDocumentNotFound()

class Revision:

    DATASOURCE_MODULE = revision
    MODULE_NAME = "revision"

    def __init__(self, language, error_if_missing=False):
        self.language = language
        self.prefix = language.__name__ + "." + self.MODULE_NAME + "."

        self.words_list = TokenFilter(
            self.prefix + "words",
            self.DATASOURCE_MODULE.tokens,
            lambda t: t.type == "word",
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

        if language.resources.stopwords is not None and \
           language.resources.stemmer is not None:
            self.infonoise = Infonoise(
                self.prefix + "infonoise",
                language.resources.stopwords,
                language.resources.stemmer.stem,
                self.words_list
            )

        if language.resources.badwords is not None:
            self.badwords_list = TextRegexExtractor(
                self.prefix + "badwords",
                self.DATASOURCE_MODULE.text,
                language.resources.badwords,
                if_none=raise_rnf if error_if_missing else None
            )

            self.badwords = Feature(
                self.prefix + "badwords", len,
                returns=int,
                depends_on=[self.badwords_list]
            )

        if language.resources.informals is not None:
            self.informals_list = TextRegexExtractor(
                self.prefix + "informals",
                self.DATASOURCE_MODULE.text,
                language.resources.informals,
                if_none=raise_rnf if error_if_missing else None
            )

            self.informals = Feature(
                self.prefix + "informals", len,
                returns=int,
                depends_on=[self.informals_list]
            )

        if language.resources.dictionary is not None:
            self.misspellings_list = TokenFilter(
                self.prefix + "misspellings",
                self.words_list,
                lambda w: not language.resources.dictionary.check(str(w))
            )

            self.misspellings = Feature(
                self.prefix + "misspellings", len,
                returns=int,
                depends_on=[self.misspellings_list]
            )
