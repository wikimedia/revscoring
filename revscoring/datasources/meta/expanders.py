from ..datasource import Datasource


class list_of(Datasource):

    def __init__(self, dependent, depends_on=None, name=None):
        name = self._format_name(name, [dependent])
        super().__init__(
            name, self.process, depends_on=depends_on)
        self.dependency = dependent

    def process(self, *lists_of_values):
        return [self.dependency(*values) for values in zip(*lists_of_values)]
