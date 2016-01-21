"""
These meta-datasources operate on :class:`revscoring.Datasource`'s that
return `list`'s and produce sub-lists.

.. autoclass:: revscoring.datasources.meta.filters.filter

.. autoclass:: revscoring.datasources.meta.filters.regex_matching

.. autoclass:: revscoring.datasources.meta.filters.positive

.. autoclass:: revscoring.datasources.meta.filters.negative
"""
import re

from ..datasource import Datasource


class filter(Datasource):
    """
    Generates a filtered list of items

    :Parameters:
        include : `func`
            A function that returns `True` when an item should be included
        items_datasource : :class:`revscoring.Datasource`
            A datasource that generates a list of items
        name : `str`
            A name for the datasource.
    """
    def __init__(self, include, items_datasource, inverse=False, name=None):
        self.include = include
        self.inverse = inverse
        name = self._format_name(name, [items_datasource])
        super().__init__(name, self.process, depends_on=[items_datasource])

    def process(self, items):
        if not self.inverse:
            return [item for item in items if self.include(item)]
        else:
            return [item for item in items if not self.include(item)]


class regex_matching(filter):
    """
    Generates a filtered list of items

    :Parameters:
        regex : `str` | `compiled re`
            A regular expression to match (case-insensitive if a `str` is
            provided)
        items_datasource : :class:`revscoring.Datasource`
            A datasource that generates a list of items
        name : `str`
            A name for the datasource.
    """
    def __init__(self, regex, strs_datasource, name=None):
        if not hasattr(regex, "pattern"):
            self.regex = re.compile(regex, re.I)
        else:
            self.regex = regex

        super().__init__(self.regex.match, strs_datasource, name=name)


class positive(filter):
    """
    Generates a filtered list of positive numbers from a list of numbers.

    :Parameters:
        numbers_datasource : :class:`revscoring.Datasource`
            A datasource that generates the subset of numbers that are positive
        name : `str`
            A name for the datasource.
    """
    def __init__(self, numbers_datasource, name=None):
        super().__init__(self.is_positive, numbers_datasource, name=name)

    def is_positive(self, v):
        return v > 0


class negative(filter):
    """
    Generates a filtered list of negative numbers from a list of numbers.

    :Parameters:
        numbers_datasource : :class:`revscoring.Datasource`
            A datasource that generates the subset of numbers that are negative
        name : `str`
            A name for the datasource.
    """
    def __init__(self, numbers_datasource, name=None):
        super().__init__(self.is_negative, numbers_datasource, name=name)

    def is_negative(self, v):
        return v < 0
