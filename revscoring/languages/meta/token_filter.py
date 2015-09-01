from ...datasources import Datasource


class TokenFilter(Datasource):

    def __init__(self, name, words_source, filter, if_none=None):
        self.filter = filter
        self.if_none = if_none
        super().__init__(name, self.process,
                         depends_on=[words_source])

    def process(self, tokens):
        if tokens is None:
            if self.if_none is not None:
                self.if_none()
            else:
                return []
        else:
            return [token for token in tokens if self.filter(token)]
