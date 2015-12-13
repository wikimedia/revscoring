from ..feature import Feature


class ItemLength(Feature):
    def __init__(self, name, items_datasource):
        super().__init__(name, self.process, returns=int,
                         depends_on=[items_datasource])

    def process(self, items):
        return len(items)
