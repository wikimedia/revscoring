from ....dependencies import DependentSet
from ....features import wikitext
from . import datasources, features


class Stopwords(DependentSet):
    """
    :Parameters:
        name : `str`
            A name for the collection
        stopword_set : `set` ( `str` )
            A set of stopwords
    """

    def __init__(self, name, stopword_set):
        super().__init__(name)
        word_is_stopword = WordIsInStopwordSet(stopword_set)

        self.revision = features.Revision(
            name + ".revision",
            datasources.Revision(name + ".revision", word_is_stopword,
                                 wikitext.revision.datasources)
        )
        """
        :class:`~revscoring.languages.features.stopwords.Revision` :
        The base revision feature set.
        """


class WordIsInStopwordSet:

    def __init__(self, stopword_set, cleanup=None):
        self.stopword_set = stopword_set

    def __call__(self, word):
        return word.lower() in self.stopword_set
