from . import datasources, features
from ....dependencies import DependentSet
from ....features import wikitext


class Dictionary(DependentSet):

    def __init__(self, name, dictionary_check):
        super().__init__(name)
        self.revision = features.Revision(
            name + ".revision",
            datasources.Revision(name + ".revision", dictionary_check,
                                 wikitext.revision.datasources)
        )
