"""
These meta-datasources operate on :class:`revscoring.Datasource`'s that returns
a list of strings (i.e. "tokens") and produces a list of ngram/skipgram
sequences.

.. autoclass:: revscoring.datasources.meta.gramming.gram

"""
from ..datasource import Datasource


class gram(Datasource):
    """
    Converts a sequence of items into ngrams.

    :Parameters:
        items_datasource : :class:`revscoring.Datasource`
            A datasource that generates a list of some item
        grams : `list` ( `tuple` ( `int` ) )
            A list of ngram and/or skipgram sequences to produce
        name : `str`
            A name for the datasource.
    """

    def __init__(self, items_datasource, grams=[(0,)], name=None):
        name = self._format_name(name, [items_datasource, grams])
        super().__init__(name, self.process,
                         depends_on=[items_datasource])
        self.grams = grams

    def process(self, tokens):
        return list(gram_tokens(tokens, grams=self.grams))


def gram_tokens(items, grams=[(0,)]):
    for i in range(len(items)):
        for gram in grams:
            if gram == (0,):
                yield (items[i], )
            elif len(items) > i + max(gram):
                yield tuple(items[i + offset] for offset in gram)
