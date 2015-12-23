from ....features.wikitext import tokenized
from .revision_oriented import StemmedDiff, StemmedRevision


class Stemmed:

    def __init__(self, prefix, stem_word):

        self.revision = StemmedRevision(
            prefix + ".revision", stem_word,
            tokenized.revision.datasources.words,
            tokenized.revision.parent.datasources.words
        )

        self.diff = StemmedDiff(
            prefix + ".diff", stem_word,
            self.revision.datasources,
            self.revision.parent.datasources
        )
