"""
Implements a feature set based off of a set of regexes applied to strings.

.. autoclass:: revscoring.languages.features.RegexMatches
    :members:
    :member-order: bysource

Implements a feature set based off of a set of substrings applied to strings.

.. autoclass:: revscoring.languages.features.SubstringMatches
    :members:
    :member-order: bysource

Supporting classes
------------------

.. autoclass:: revscoring.languages.features.matches.Revision
    :members:
    :member-order: bysource

.. autoclass:: revscoring.languages.features.matches.Diff
    :members:
    :member-order: bysource
"""
from .features import Diff, Revision
from .matches import Matches
from .substring_matches import SubstringMatches
from .regex_matches import RegexMatches

__all__ = [Matches, RegexMatches, SubstringMatches, Revision, Diff]
