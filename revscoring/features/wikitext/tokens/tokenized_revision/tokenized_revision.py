from ....meta import aggregators
from ..tokenized import tokenized
from .datasources import Datasources


class TokenizedRevision:

    def __init__(self, prefix, text_datasource=None, tokens_datasource=None):

        if tokens_datasource is None:
            if text_datasource is None:
                raise TypeError("Either text or tokens must be specified.")
            else:
                tokens_datasource = tokenized(text_datasource)

        self.datasources = Datasources(prefix, tokens_datasource)

        self.tokens = aggregators.len(self.datasources.tokens)
        self.numbers = aggregators.len(self.datasources.numbers)
        self.whitespaces = aggregators.len(self.datasources.whitespaces)
        self.markups = aggregators.len(self.datasources.markups)
        self.cjks = aggregators.len(self.datasources.cjks)
        self.entities = aggregators.len(self.datasources.entities)
        self.urls = aggregators.len(self.datasources.urls)
        self.words = aggregators.len(self.datasources.words)
        self.uppercase_words = \
            aggregators.len(self.datasources.uppercase_words)
        self.punctuations = aggregators.len(self.datasources.punctuations)
        self.breaks = aggregators.len(self.datasources.breaks)
