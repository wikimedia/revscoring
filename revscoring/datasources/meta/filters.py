import re

from .meta_datasource import MetaDatasource


class filter(MetaDatasource):

    def __init__(self, include, items_datasource, name=None):
        self.include = include
        name = self.format_name(name, [items_datasource])
        super().__init__(name, depends_on=[items_datasource])

    def process(self, items):
        return [item for item in items if self.include(item)]


class regex_matching(filter):

    def __init__(self, regex, strs_datasource, name=None):
        if not hasattr(regex, "pattern"):
            self.regex = re.compile(regex, re.I)
        else:
            self.regex = regex

        super().__init__(name, self.match, strs_datasource)

    def match(self, s):
        return bool(self.regex.match(s))


class positive(filter):

    def __init__(self, number_datasource, name=None):
        super().__init__(name, self.is_positive, number_datasource)

    def is_positive(self, v):
        return v > 0


class negative(filter):

    def __init__(self, number_datasource, name=None):
        super().__init__(name, self.is_positive, number_datasource)

    def is_positive(self, v):
        return v < 0
