"""
These Meta-Features apply return a simple boolean value

.. autoclass revscoring.features.meta.bools.regex_match

.. autoclass revscoring.features.meta.bools.item_in_set

.. autoclass revscoring.features.meta.bools.set_contains_item

.. autoclass revscoring.features.meta.bools.sets_intersect
"""
import re

from ..feature import Feature


class regex_match(Feature):
    """
    Constructs a :class:`revscoring.Feature` that return `True` when
    `string_datasource` is matched by `regex`.

    :Parameters:
        regex : `str` | `re.compile`
            A regular expression to use when matching
        string_datasource : :class:`revscoring.Datasource`
            A datasource that returns a string to use in matching
        name : `str`
            A name for the feature
    """

    def __init__(self, regex, string_datasource, name=None):
        if not hasattr(regex, 'pattern'):
            regex = re.compile(regex, re.I)

        self.regex = regex

        name = self._format_name(name, [regex.pattern, string_datasource])
        super().__init__(name, self.process, depends_on=[string_datasource],
                         returns=bool)

    def process(self, s):
        return bool(self.regex.match(s))


class item_in_set(Feature):
    """
    Constructs a :class:`revscoring.Feature` that return `True` when
    `item` appears in `set`.

    :Parameters:
        item : `hashable`
            An item to look for in `items_datasource`
        items_datasource : :class:`revscoring.Datasource`
            A datasource that returns a set of items
        name : `str`
            A name for the feature
    """

    def __init__(self, item, items_datasource, name=None):
        self.item = item
        name = self._format_name(name, [item, items_datasource])
        super().__init__(name, self.process, depends_on=[items_datasource],
                         returns=bool)

    def process(self, items):
        return self.item in set(items or [])


class set_contains_item(Feature):
    """
    Constructs a :class:`revscoring.Feature` that return `True` when
    `items` contains the item returned by `item_datasource`.

    :Parameters:
        items : `set` ( `hashable` )
            An item to look for in `items_datasource`
        item_datasource : :class:`revscoring.Datasource`
            A datasource that returns a `hashable` item
        name : `str`
            A name for the feature
    """

    def __init__(self, items, item_datasource, name=None):
        self.items = set(items)
        name = self._format_name(name, [items, item_datasource])
        super().__init__(name, self.process, depends_on=[item_datasource],
                         returns=bool)

    def process(self, item):
        return item in set(self.items)


class sets_intersect(Feature):
    """
    Constructs a :class:`revscoring.Feature` that return `True` when
    `items` contains any item returned by `item_datasource`.

    :Parameters:
        items : `set` ( `hashable` )
            An set of items to look for in `items_datasource`
        items_datasource : :class:`revscoring.Datasource`
            A datasource that returns a collection of items
        name : `str`
            A name for the feature
    """

    def __init__(self, items, items_datasource, name=None):
        self.items = set(items)
        name = self._format_name(name, [items, items_datasource])
        super().__init__(name, self.process, depends_on=[items_datasource],
                         returns=bool)

    def process(self, items):
        return len(set(items or []) & self.items) > 0
