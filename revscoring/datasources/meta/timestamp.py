"""
These meta-datasources operate on :class:`revscoring.Datasource`'s that
return `mwtypes.Timestamp` of the given string.

.. autoclass:: revscoring.datasources.meta.timestamp.Timestamp
"""
import mwtypes

from ..datasource import Datasource

MW_REGISTRATION_EPOCH = '2006-01-01T00:00:00Z'


class Timestamp(Datasource):
    """
    Generates a mwtypes.Timestamp of the given string

    :Parameters:
        timestamp_str : `str`
            Timestamp string in ISO format.
        name : `str`
            A name for the datasource.
    """

    def __init__(self, timestamp_str, name=None):
        super().__init__(name, self.process,
                         depends_on=[timestamp_str])

    def process(self, timestamp_str):
        return mwtypes.Timestamp(timestamp_str or MW_REGISTRATION_EPOCH)
