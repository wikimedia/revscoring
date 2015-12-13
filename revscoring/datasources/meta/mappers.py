from ..datasource import Datasource


class map(Datasource):

    def __init__(self, apply, items_datasource, name=None):
        self.apply = apply
        name = self.format_name(name, [items_datasource])
        super().__init__(name, self.process, depends_on=[items_datasource])

    def process(self, items):
        return [self.apply(item) for item in items]


class lower_case(map):

    def __init__(self, strs_datasource, name=None):
        name = self.format_name(name, [strs_datasource])
        super().__init__(name, self.lower, strs_datasource)

    def lower(self, s):
        return s.lower()


class abs(map):

    def __init__(self, numbers_datasource, name=None):
        super().__init__(name, self.absify, numbers_datasource)

    def absify(self, v):
        return abs(v)
