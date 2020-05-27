"""
Dictionary
++++++++++
.. automodule :: revscoring.languages.features.dictionary

RegexMatches
++++++++++++
.. automodule :: revscoring.languages.features.matches.regex_matches

Stopwords
+++++++++
.. automodule :: revscoring.languages.features.stopwords

Stemmed
+++++++
.. automodule :: revscoring.languages.features.stemmed

SubstringMatches
++++++++++++++++
.. automodule :: revscoring.languages.features.matches.substring_matches

"""
from .dictionary import Dictionary
from .stemmed import Stemmed
from .stopwords import Stopwords
from .matches.regex_matches import RegexMatches
from .matches.substring_matches import SubstringMatches

__all__ = [Dictionary, RegexMatches, Stemmed, Stopwords, SubstringMatches]
