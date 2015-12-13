from ...feature import Feature


class MetaFeature(Feature):

    def __init__(self, returns, depends_on=None, name=None):
        if name is None:
            name = "{0}({1})".format(self.__class__.__name__,
                                     self.items_datasource)

        super().__init__(name, self.process, depends_on=depends_on,
                         returns=returns)
