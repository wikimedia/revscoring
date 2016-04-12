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
        wrapping : `tuple` ( `str`, `str` )
            Insert these characters around matches in the regular expression
    """

    def __init__(self, name, regexes, wrapping=(r'\b', r'\b')):
        super().__init__(name)
        self.revision = features.Revision(
            name + ".revision", regexes,
            datasources.Revision(
                name + ".revision", regexes,
                wikitext.revision.datasources,
                wrapping=wrapping
            )
        )
        """
        :class:`~revscoring.languages.features.regex_matches.Revision` :
        The base revision feature set.
        """
