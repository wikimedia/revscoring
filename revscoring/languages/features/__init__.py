"""
.. autoclass :: revscoring.features.Dictionary
    :members:

.. autoclass :: revscoring.features.RegexMatches
    :members:

.. autoclass :: revscoring.features.Stopwords
    :members:

.. autoclass :: revscoring.features.Stemmed
    :members:
"""
from .dictionary import Dictionary
from .regex_matches import RegexMatches
from .stemmed import Stemmed
from .stopwords import Stopwords

__all__ = [Dictionary, RegexMatches, Stemmed, Stopwords]
