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
import re

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
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

class RegexLanguage(Language):

    def __init__(self, name, badwords=None, informals=None, dictionary=None,
                       stemmer=None, stopwords=None):
        cache = {}
        if badwords is not None:
            self.badword_re = re.compile("|".join(badwords), re.I)
            cache[is_badword] = self.is_badword

        if informals is not None:
            self.informal_re = re.compile("|".join(informals), re.I)
            cache[is_informal_word] = self.is_informal_word

        if dictionary is not None:
            self.dictionary = dictionary
            cache[is_misspelled] = self.is_misspelled

        if stemmer is not None:
            self.stemmer = stemmer
            cache[stem_word] = self.stem_word

        if stopwords is not None:
            self.stopwords = set(stopwords)
            cache[is_stopword] = self.is_stopword

        super().__init__(name, cache=cache)


    def is_badword(self, word):
        return bool(self.badword_re.match(word))

    def is_informal_word(self, word):
        return bool(self.informal_re.match(word))

    def stem_word(self, word):
        return self.stemmer.stem(word)

    def is_misspelled(self, word):
        return not self.dictionary.check(word)

    def is_stopword(self, word):
        return word.lower() in self.stopwords





class LanguageUtility(dependencies.Dependent):
    """
    Implements a dependency wrapper for a utility functions.
    """

    def __hash__(self):
        return hash(('language_utility', self.name))

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

is_informal_word = LanguageUtility("is_informal_word")
"""
Returns a boolean value that is `True` when a given word is not encyclopaedic
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
