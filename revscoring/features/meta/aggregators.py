from ..feature import Feature


class sum(Feature):
    def __init__(self, items_datasource, name=None):
        name = self._format_name(name, [items_datasource])
        super().__init__(name, self.process, depends_on=[items_datasource],
                         returns=float)

    def process(self, items):
        return sum(items)


class len(Feature):
    def __init__(self, items_datasource, name=None):
        name = self._format_name(name, [items_datasource])
        super().__init__(name, self.process, depends_on=[items_datasource],
                         returns=int)

    def process(self, items):
        return len(items)
