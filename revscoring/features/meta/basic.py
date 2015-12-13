from .meta_feature import MetaFeature


class sum(MetaFeature):
    def __init__(self, items_datasource, name=None):
        super().__init__(depends_on=[items_datasource], returns=float,
                         name=name)

    def process(self, items):
        return sum(items)


class len(MetaFeature):
    def __init__(self, items_datasource, name=None):
        super().__init__(depends_on=[items_datasource], returns=float,
                         name=name)

    def process(self, items):
        return len(items)
