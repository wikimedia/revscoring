from . import datasources, features
from ....dependencies import DependentSet
from ....features import wikitext


class RegexMatches(DependentSet):
    """
    :Parameters:
        name : `str`
            A name for the collection
        regexes : `list` ( `str` )
            A list of regex patterns to match.
        use_word_boundaries : `bool`
            If true, insert word boundary chars before and after regexes.
    """

    def __init__(self, name, regexes, use_word_boundaries=True):
        super().__init__(name)
        self.revision = features.Revision(
            name + ".revision", regexes,
            datasources.Revision(
                name + ".revision", regexes,
                wikitext.revision.datasources,
                use_word_boundaries
            )
        )
        """
        :class:`~revscoring.languages.features.regex_matches.Revision` :
        The base revision feature set.
        """
