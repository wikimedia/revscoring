import re

from ...datasources import Datasource


class TokenFilter(Datasource):

    def __init__(self, name, tokens_datasource, filter, if_none=None):
        self.filter = filter
        self.if_none = if_none
        super().__init__(name, self.process,
                         depends_on=[tokens_datasource])

    def process(self, tokens):
        if tokens is None:
            if self.if_none is not None:
                self.if_none()
            else:
                return []
        else:
            return [token for token in tokens if self.filter(token)]


class TokensMatching(TokenFilter):

    def __init__(self, name, tokens_datasource, regex, regex_flags=re.I,
                 if_none=None):
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, regex_flags)

        filter = lambda t: regex.match(t)

        super().__init__(name, tokens_datasource, filter, if_none=if_none)
