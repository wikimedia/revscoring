from ..datasource import Datasource


class dict_keys(Datasource):

    def __init__(self, name, dict_datasource):
        name = self.format_name(name, [dict_datasource])
        super().__init__(name, self.process,
                         depends_on=[dict_datasource])

    def process(self, d):
        return d.keys()


class dict_values(Datasource):

    def __init__(self, name, dict_datasource):
        name = self.format_name(name, [dict_datasource])
        super().__init__(name, self.process,
                         depends_on=[dict_datasource])

    def process(self, d):
        return d.values()
