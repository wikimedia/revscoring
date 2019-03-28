"""
Implements a feature set based off of stemmer applied to words.

.. autoclass:: revscoring.languages.features.Stemmed
    :members:
    :member-order: bysource

Supporting classes
------------------

.. autoclass:: revscoring.languages.features.stemmed.Revision
    :members:
    :member-order: bysource

.. autoclass:: revscoring.languages.features.stemmed.Diff
    :members:
    :member-order: bysource
"""
from .features import Diff, Revision
from .stemmed import Stemmed

__all__ = [Stemmed, Revision, Diff]
