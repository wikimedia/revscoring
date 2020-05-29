"""
Implements a feature set based off of list of regular expressions to match.

.. autoclass:: revscoring.languages.features.SubstringMatches
    :members:
    :member-order: bysource
"""
from . import Matches
from ....datasources.meta import extractors


class SubstringMatches(Matches):
    """
    :Parameters:
        name : `str`
            A name for the collection
        substrings : `list` ( `str` )
            A list of substrings to match.
        exclusions : `list` ( `str` )
            A list of substrings to explicitly not match
    """

    def __init__(self, name, substrings, exclusions=None,
                 text_preprocess=None):
        matcher = extractors.trie(substrings,
                                  exclusions=exclusions).process
        super().__init__(name, matcher, substrings, exclusions,
                         text_preprocess=text_preprocess)
