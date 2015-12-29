from ..feature import Feature


class item_in_set(Feature):
    def __init__(self, item, items_datasource, name=None):
        self.item = item
        name = self._format_name(name, [item, items_datasource])
        super().__init__(name, self.process, depends_on=[items_datasource],
                         returns=bool)

    def process(self, items):
        return self.item in items
