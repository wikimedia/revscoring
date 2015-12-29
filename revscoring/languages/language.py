"""
.. autoclass:: revscoring.Language
"""
from ..dependencies import DependentSet


class Language(DependentSet):
    """
    Implements a set of language-specific features.

    :Parameters:
        name : str
            A name for the language.  Note that this name will be used when
            comparing languages to each other.
    """
    def __init__(self, name, doc=None):
        self.name = name
        self.__name__ = name
        self.__doc__ = doc
