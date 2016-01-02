import re

from ..feature import Feature


class regex_match(Feature):
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
    def __init__(self, item, items_datasource, name=None):
        self.item = item
        name = self._format_name(name, [item, items_datasource])
        super().__init__(name, self.process, depends_on=[items_datasource],
                         returns=bool)

    def process(self, items):
        return self.item in set(items or [])


class set_contains_item(Feature):
    def __init__(self, items, item_datasource, name=None):
        self.items = set(items)
        name = self._format_name(name, [items, item_datasource])
        super().__init__(name, self.process, depends_on=[item_datasource],
                         returns=bool)

    def process(self, item):
        return item in set(self.items)


class sets_intersect(Feature):
    def __init__(self, items, items_datasource, name=None):
        self.items = set(items)
        name = self._format_name(name, [items, items_datasource])
        super().__init__(name, self.process, depends_on=[items_datasource],
                         returns=bool)

    def process(self, items):
        return len(set(items or []) & self.items) > 0
