"""
These Meta-Features genetate a :class:`revscoring.FeatureVector` based on some
:class:`revscoring.Datasource`.

.. autoclass revscoring.features.meta.vectorizers.vectorize
"""
from ..feature_vector import FeatureVector


class vectorize(FeatureVector):
    """
    Constructs a :class:`revscoring.FeatureVector` that converts a
    dictionary into a list of values with a predictable order based on a set of
    keys.

    :Parameters:
        dict_datasource : :class:`revscoring.Datasource`
            A datasource that returns a dictionary of values.  If the
            datasource implements a `keys()` method, that will be used for
            selecting keys to vectorize
        keys : `iterable` ( `hashable` )
            A collection of keys to be vectorized from the dictionary.  If
            specified, this will override the `keys()` method on the
            `dict_datasource`
        returns : `func`
            A function that represents the type of value that will be
            contained in the vector.  When called without an argument, this
            function should return the default value (for missing) keys
            in the dict.
        name : `str`
            A name for the `revscoring.FeatureVector`
    """

    def __init__(self, dict_datasource, keys=None, returns=None, name=None):
        if keys is None:
            if hasattr(dict_datasource, "keys"):
                keys = dict_datasource.keys()
            else:
                raise AttributeError(
                    "{0} does not have a keys() ".format(dict_datasource) +
                    "method and `keys` argument was not specified")

        self.keys = sorted(keys) if keys is not None else None
        name = self._format_name(name, [dict_datasource, self.keys[:10]])
        super().__init__(name, self.process, depends_on=[dict_datasource],
                         returns=returns)
        # Sorting keys so that output is deterministic

    def process(self, d):

        return [(d[key] if key in d else self.returns()) for key in self.keys]
