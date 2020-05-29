from . import datasources, features
from ....dependencies import DependentSet
from ....features import wikitext


class Matches(DependentSet):
    def __init__(self, name, matcher, match_list, exclusions=None,
                 text_preprocess=None):
        super().__init__(name)
        self._match_list = match_list
        self._exclusions = exclusions
        self.revision = features.Revision(
            name + ".revision",
            datasources.Revision(
                name + ".revision", matcher,
                wikitext.revision.datasources,
                text_preprocess=text_preprocess
            )
        )
        """
        :class:`~revscoring.languages.features.matches.Revision` :
        The base revision feature set.
        """

    def excluding(self, exclusions, name=None):
        """
        Returns a new :class:`~revscoring.languages.features.Matches`
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
            self._match_list,
            exclusions=(self._exclusions or []) + exclusions)
