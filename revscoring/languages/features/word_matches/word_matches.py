from . import datasources, features
from ....dependencies import DependentSet
from ....features import wikitext


class WordMatches(DependentSet):
    """
    :Parameters:
        name : `str`
            A name for the collection
        words : `list` ( `str` )
            A list of words to match.
    """

    def __init__(self, name, words):
        super().__init__(name)

        self.revision = features.Revision(
            name + ".revision", words,
            datasources.Revision(
                name + ".revision", words,
                wikitext.revision.datasources)
        )
        """
        :class:`~revscoring.languages.features.word_matches.Revision` :
        The base revision feature set.
        """
