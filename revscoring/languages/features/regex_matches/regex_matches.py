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
        exclusions : `list` ( `str` )
            A list of terms to explicitly not match
        wrapping : `tuple` ( `str`, `str` )
            Insert these characters around matches in the regular expression
    """

    def __init__(self, name, regexes, exclusions=None,
                 wrapping=(r'\b', r'\b')):
        super().__init__(name)
        self._regexes = regexes
        self._exclusions = exclusions
        self._wrapping = wrapping
        self.revision = features.Revision(
            name + ".revision", regexes,
            datasources.Revision(
                name + ".revision", regexes,
                wikitext.revision.datasources,
                exclusions=exclusions,
                wrapping=wrapping
            )
        )
        """
        :class:`~revscoring.languages.features.regex_matches.Revision` :
        The base revision feature set.
        """

    def excluding(self, exclusions, name=None):
        """
        Returns a new :class:`~revscoring.languages.features.RegexMatches`
        that includes a set of exclusions.

        :Parameters:
            exclusions : `list` ( `str` )
                A list of terms to explicitly not match
            name : `str`
                A new name for the collection.  If unspecified, the old name
                will be used
        """
        return self.__class__(
            name or self._name + ".excluding({0!r})".format(exclusions),
            self._regexes,
            exclusions=(self._exclusions or []) + exclusions,
            wrapping=self._wrapping)
