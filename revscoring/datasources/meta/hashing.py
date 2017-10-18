"""
These meta-datasources operate on :class:`revscoring.Datasource`'s that returns
a list of strings (i.e. "tokens") and produces a list of ngram/skipgram
sequences.

.. autoclass:: revscoring.datasources.meta.hashing.hash

"""
import json

import mmh3

from ..datasource import Datasource


class hash(Datasource):
    """
    Converts a sequence of items into a sequence of portable hashes (`int`)
    based on the result of applying `str()`.  E.g. `str(["foo"]) = '["foo"]'`

    :Parameters:
        items_datasource : :class:`revscoring.Datasource`
            A datasource that generates a list of items to be hashed
        n : `int`
            The number of potential hashes that can be produced
        name : `str`
            A name for the datasource.
    """

    def __init__(self, items_datasource, n=2 ** 20, name=None):
        name = self._format_name(name, [items_datasource, n])
        super().__init__(name, self.process,
                         depends_on=[items_datasource])
        self.n = n

    def process(self, items):
        return [mmh3_item(item, self.n) for item in items]


def mmh3_item(item, n):
    return (2**32 + mmh3.hash(json.dumps(item))) % n
