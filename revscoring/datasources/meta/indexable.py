"""
These meta-datasources operate on :class:`revscoring.Datasource`'s that
return `list`'s and `tuple`'s

.. autoclass:: revscoring.datasources.meta.index

"""
from ..datasource import Datasource


class index(Datasource):
    """
    Generates a datasource that returns the value that appears at `i`

    :Parameters:
        i : `int`
            The index of a value to return
        default : `mixed`
            The value to return if no value exists at `i`.  If not specified,
            an IndexError will be raised
        name : `str`
            A name for the new datasource.
    """
    def __init__(self, i, datasources, default=NotImplemented, name=None):
        name = self._format_name(name, [i, default])
        self.i = int(i)
        self.default = default
        super().__init__(name, self.process,
                         depends_on=[datasources])

    def process(self, indexable):
        try:
            return indexable[self.i]
        except IndexError:
            if self.default is not NotImplemented:
                return self.default
            else:
                raise
