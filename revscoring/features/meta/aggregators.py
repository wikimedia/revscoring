from ..feature import Feature

len_builtin = len
sum_builtin = sum
max_builtin = max
min_builtin = min


class sum(Feature):
    def __init__(self, items_datasource, name=None, returns=float):
        name = self._format_name(name, [items_datasource])
        super().__init__(name, self.process, depends_on=[items_datasource],
                         returns=returns)

    def process(self, items):
        return self.returns(sum_builtin(items))


class len(Feature):
    def __init__(self, items_datasource, name=None):
        name = self._format_name(name, [items_datasource])
        super().__init__(name, len_builtin, depends_on=[items_datasource],
                         returns=int)


class max(Feature):
    def __init__(self, items_datasource, name=None, returns=float):
        name = self._format_name(name, [items_datasource])
        super().__init__(name, self.process, depends_on=[items_datasource],
                         returns=returns)

    def process(self, items):
        if len(items) == 0:
            return self.returns()
        else:
            return self.returns(max_builtin(items))


class min(Feature):
    def __init__(self, items_datasource, name=None, returns=float):
        name = self._format_name(name, [items_datasource])
        super().__init__(name, self.process, depends_on=[items_datasource],
                         returns=returns)

    def process(self, items):
        if len(items) == 0:
            return self.returns()
        else:
            return self.returns(min_builtin(items))
