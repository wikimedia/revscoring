"""
Utilities:

.. autodata:: revscoring.languages.language.stem_word
.. autodata:: revscoring.languages.language.is_badword
.. autodata:: revscoring.languages.language.is_misspelled
.. autodata:: revscoring.languages.language.is_stopword

Base classes:

.. autoclass:: revscoring.languages.language.Language
    :members:

.. autoclass:: revscoring.languages.language.LanguageUtility
    :members:
"""
import yamlconf

from .. import dependencies


class Language(dependencies.Context):
    """
    Constructs a context for providing language utilities to a dependency
    solver.

    :Parameters:
        name : str
            An identifier for the language (e.g., "english")
        utilities : `iterable`
            A collection of
            :class:`revscoring.languages.language.LanguageUtility`
    """
    def __init__(self, name, utilities):
        super().__init__(context=utilities)
        self.name = str(name)

    def __eq__(self, other):
        try:
            return self.name == other.name and \
                   self.context == other.context
        except AttributeError as e:
            return False

    @classmethod
    def from_config(self, config, name, section_key="languages"):
        """
        Constructs a :class:`revscoring.languages.language.Language` from a
        `dict`.

        :Parameters:
            config : dict
                A configuration dictionary
            name : str
                The name of the sub-section in which to look for configuration
                information
            section_key : str
                The top-level section key under which to look for `name`
        """
        section = config[section_key][name]
        if 'module' in section:
            return yamlconf.import_module(section['module'])
        elif 'class' in section:
            raise RuntimeError("Loading a language via class construction " + \
                               "not yet supported")


class LanguageUtility(dependencies.Dependent):
    """
    Implements a dependency wrapper for a utility functions.
    """
    pass

# Define placeholder utilities.  These will need to be replaced inside of a
# language, but they will provide names to match against within the cache.
stem_word = LanguageUtility("stem_word")
"""
Converts a word to it's stem.  E.g. "running" --> "run"
"""

is_badword = LanguageUtility("is_badword")
"""
Returns a boolean value that is `True` when a given word is "bad" or generally
realted to damaging edits
"""

is_misspelled = LanguageUtility("is_misspelled")
"""
Returns a boolean value that is `True` when a given word cannot be found in
a relevant dictionary.
"""

is_stopword = LanguageUtility("is_stopword")
"""
Returns a boolean value that is `True` when a given word is a 'stopword' --
i.e., common and unimportant to the informational properties of a text.
"""
