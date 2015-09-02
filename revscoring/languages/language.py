"""
.. autoclass:: revscoring.languages.language.Language
"""


class Language:
    """
    Implements a set of language-specific features.

    :Parameters:
        name : str
            A name for the language.  Note that this name will be used when
            comparing languages to each other.
    """
    def __init__(self, name, doc=None):
        self.__name__ = name
        self.__doc__ = doc if doc else name

    def __eq__(self, other):
        return isinstance(other, Language) and self.__name__ == other.__name__
