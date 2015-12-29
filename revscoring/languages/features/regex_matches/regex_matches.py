from . import datasources, features
from ....dependencies import DependentSet
from ....features import wikitext


class RegexMatches(DependentSet):

    def __init__(self, name, regexes):
        super().__init__(name)
        self.revision = features.Revision(
            name + ".revision", regexes,
            datasources.Revision(
                name + ".revision", regexes,
                wikitext.revision.datasources
            )
        )
