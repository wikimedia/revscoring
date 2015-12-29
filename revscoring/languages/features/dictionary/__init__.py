"""
Implements a feature set based off of dictionary lookup.

.. autoclass:: revscoring.languages.features.Dictionary
    :members:
    :member-order: bysource

Supporting classes
------------------

.. autoclass:: revscoring.languages.features.dictionary.Revision
    :members:
    :member-order: bysource

.. autoclass:: revscoring.languages.features.dictionary.Diff
    :members:
    :member-order: bysource
"""
from .dictionary import Dictionary
from .features import Diff, Revision
from .util import utf16_cleanup

__all__ = [Dictionary, utf16_cleanup, Revision, Diff]
