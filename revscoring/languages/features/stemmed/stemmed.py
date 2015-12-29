from . import datasources, features
from ....dependencies import DependentSet
from ....features import wikitext


class Stemmed(DependentSet):

    def __init__(self, name, stem_word):
        super().__init__(name)
        self.revision = features.Revision(
            name + ".revision",
            datasources.Revision(name + ".revision", stem_word,
                                 wikitext.revision.datasources)
        )
