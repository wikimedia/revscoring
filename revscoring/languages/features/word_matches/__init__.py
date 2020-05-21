"""
Implements a feature set based off of a set of word or phrases applied to strings.

.. autoclass:: revscoring.languages.features.WordMatches
    :members:
    :member-order: bysource

Supporting classes
------------------

.. autoclass:: revscoring.languages.features.word_matches.Revision
    :members:
    :member-order: bysource

.. autoclass:: revscoring.languages.features.word_matches.Diff
    :members:
    :member-order: bysource
"""
from .features import Diff, Revision
from .word_matches import WordMatches

__all__ = [WordMatches, Revision, Diff]
