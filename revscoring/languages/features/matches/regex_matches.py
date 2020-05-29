"""
Implements a feature set based off of list of regular expressions to match.

.. autoclass:: revscoring.languages.features.RegexMatches
    :members:
    :member-order: bysource
"""
from . import Matches
from ....datasources.meta import extractors


class RegexMatches(Matches):
    """
    :Parameters:
        name : `str`
            A name for the collection
        regexes : `list` ( `str` )
            A list of regex patterns to match.
        exclusions : `list` ( `str` )
            A list of terms to explicitly not match
        wrapping : `tuple` ( `str`, `str` )
            Insert these characters around matches in the regular expression
    """

    def __init__(self, name, regexes, exclusions=None,
                 wrapping=(r'\b', r'\b'), text_preprocess=None):
        matcher = extractors.regex(regexes, wrapping=wrapping,
                                   exclusions=exclusions).process
        super().__init__(name, matcher, regexes, exclusions,
                         text_preprocess)
