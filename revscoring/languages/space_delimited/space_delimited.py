from collections import namedtuple

from ..language import Language
from .diff import Diff
from .parent_revision import ParentRevision
from .revision import Revision

Resources = namedtuple(
    "Resources",
    ['badwords', 'dictionary', 'informals', 'stemmer', 'stopwords']
)

class SpaceDelimited(Language):

    """
    Implements a set of useful features for a space-delimited class of language.
    """
    def __init__(self, name, badwords=None, dictionary=None, informals=None,
                 stemmer=None, stopwords=None):
        super().__init__(name)
        self.prefix = name
        stopwords = set(stopwords) if stopwords is not None else None
        self.resources = Resources(badwords, dictionary, informals, stemmer,
                                   stopwords)

        self.diff = Diff(self)
        self.parent_revision = ParentRevision(self)
        self.revision = Revision(self)
