from . import datasources, features
from ....features import wikitext


class Dictionary:

    def __init__(self, name, dictionary_check):
        self.revision = features.Revision(
            name + ".revision",
            datasources.Revision(name + ".revision", dictionary_check,
                                 wikitext.revision.datasources)
        )
