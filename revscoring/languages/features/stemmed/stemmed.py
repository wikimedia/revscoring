from . import datasources, features
from ....dependencies import DependentSet
from ....features import wikitext


class Stemmed(DependentSet):
    """
    :Parameters:
        name : `str`
            A name for the collection
        stem_word : `func`
            A function that, give a word, will return a stemmed version of that
            word
    """

    def __init__(self, name, stem_word):
        super().__init__(name)
        self.revision = features.Revision(
            name + ".revision",
            datasources.Revision(name + ".revision", stem_word,
                                 wikitext.revision.datasources)
        )
        """
        :class:`~revscoring.languages.features.stemmed.Revision` :
        The base revision feature set.
        """
