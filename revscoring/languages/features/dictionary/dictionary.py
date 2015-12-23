from ....features.wikitext import tokenized
from .revision_oriented import DictionaryDiff, DictionaryRevision


class Dictionary:

    def __init__(self, prefix, dictionary_check):
        self.revision = DictionaryRevision(
            prefix + ".revision", dictionary_check,
            tokenized.revision.datasources.words,
            tokenized.revision.parent.datasources.words
        )
        self.diff = DictionaryDiff(
            prefix + ".diff", dictionary_check,
            self.revision.datasources,
            self.revision.parent.datasources
        )
