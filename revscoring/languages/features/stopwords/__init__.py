"""
Implements a feature set based off of filtering words for stopwords

.. autoclass:: revscoring.languages.features.Stopwords
    :members:
    :member-order: bysource

Supporting classes
------------------

.. autoclass:: revscoring.languages.features.stopwords.Revision
    :members:
    :member-order: bysource

.. autoclass:: revscoring.languages.features.stopwords.Diff
    :members:
    :member-order: bysource
"""
from .features import Diff, Revision
from .stopwords import Stopwords

__all__ = [Stopwords, Revision, Diff]
