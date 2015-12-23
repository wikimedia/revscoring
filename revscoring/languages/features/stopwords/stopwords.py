from ....features.wikitext import tokenized
from .revision_oriented import StopwordsDiff, StopwordsRevision


class Stopwords:

    def __init__(self, prefix, stopwords_set):
        self.revision = StopwordsRevision(
            prefix + ".stopwords.revision", stopwords_set,
            tokenized.revision.datasources.words,
            tokenized.revision.parent.datasources.words
        )

        self.diff = StopwordsDiff(
            prefix + ".stopwords.diff", stopwords_set,
            self.revision.datasources,
            self.revision.parent.datasources
        )
