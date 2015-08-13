from ...datasources import Datasource


class Constant(Datasource):

    def __init__(self, name, value):
        self.value = value
        super().__init__(name, self.process)

    def process(self):
        return self.value
