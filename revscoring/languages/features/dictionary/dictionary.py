from . import datasources, features
from ....dependencies import DependentSet
from ....features import wikitext


class Dictionary(DependentSet):
    """
    :Parameters:
        name : `str`
            A name for the collection
        dictionary_check : `func`
            A function that, given a word, performs a dictionary check and
            returns True if the word exists.
    """

    def __init__(self, name, dictionary_check):
        super().__init__(name)
        self.revision = features.Revision(
            name + ".revision",
            datasources.Revision(name + ".revision", dictionary_check,
                                 wikitext.revision.datasources)
        )
        """
        :class:`~revscoring.languages.features.dictionary.Revision` :
        The base revision feature set.
        """
