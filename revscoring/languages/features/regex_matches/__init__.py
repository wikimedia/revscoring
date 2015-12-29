"""
Implements a feature set based off of a set of regexes applied to strings.

.. autoclass:: revscoring.languages.features.RegexMatches
    :members:
    :member-order: bysource

Supporting classes
------------------

.. autoclass:: revscoring.languages.features.regex_matches.Revision
    :members:
    :member-order: bysource

.. autoclass:: revscoring.languages.features.regex_matches.Diff
    :members:
    :member-order: bysource
"""
from .regex_matches import RegexMatches
from .features import Revision, Diff

__all__ = [RegexMatches, Revision, Diff]
