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
    Implements a set of useful features for a space-delimited class of
    language.

    Features are made available depending on the arguments provided to the
    constructor.  Reference the language implementation for available features.

    :Parameters:
        name : str
            The name of the language.  Not that this name will be used when
            checking for equality between languages.
        badwords : `list` of `str`
            A list of regexes to be used to match badwords.  Note that word
            boundary characters will be placed around your regex.
            E.g. `r"\\\\bbadword\\\\b"`
        dictionary : :class:`enchant.Dict`
            An enchant dictionary for use in looking up words
        informals : `list` of `str`
            A list of regexes to be used to match informal words.  Like
            badwords, these regexes will be wrapped in word boundary
            characters.
        stemmer : :class:`nltk.stem.api.StemmerI`
            An nltk-based stemmer to be used to remove morphological affixes
            from words.
        stopwords : `set` of `str`
            A set of common words to use when processing the informational
            content of text.  See `stopwords` in `nltk.corpus`.
    """
    def __init__(self, name, doc=None, badwords=None, dictionary=None,
                 informals=None, stemmer=None, stopwords=None):
        super().__init__(name, doc=doc)
        self.prefix = name
        stopwords = set(stopwords) if stopwords is not None else None
        self.resources = Resources(badwords, dictionary, informals, stemmer,
                                   stopwords)
        """
        The set of resources that were made available to the constructor
        """

        self.diff = Diff(self)
        """
        A module containing language-specific, diff-based features
        """

        self.parent_revision = ParentRevision(self)
        """
        A module containing language-specific, parent revision-based features
        """

        self.revision = Revision(self)
        """
        A module containing language-specific, revision-based features
        """
