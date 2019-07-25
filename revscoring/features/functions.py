"""
.. autofunction:: revscoring.features.trim
"""
from itertools import chain

from .feature import Constant, Feature, Modifier


def trim(features, context=None):
    """
    Trims a feature set down to a bare set of :class:`~revscoring.Feature` by
    removing :class:`~revscoring.features.Modifier` and
    :class:`~revscoring.features.Constant`.

    :Parameters:
        features : `list` ( :class:`revscoring.Feature` )
            A feature list to trim
        context : `dict` | `set`
            A context to apply while trimming
    """
    context = context or {}
    cache = set()

    if hasattr(features, "__iter__"):
        for feature in features:
            yield from _trim(feature, context, cache)
    else:
        yield from _trim(features, context, cache)


def _trim(dependent, context, cache):
    if isinstance(dependent, Feature):
        feature = dependent
        if isinstance(feature, Modifier):
            for dependent in feature.dependencies:
                yield from _trim(dependent, context, cache)
        elif isinstance(feature, Constant):
            pass
        else:
            if feature not in cache:
                cache.add(feature)
                yield feature


def vectorize_values(feature_values):
    """
    Converts a list of feature_values that contains sub-FeatureVector
    into a flat list of values.
    """
    return list(chain(*(val if hasattr(val, "__iter__") else [val]
                        for val in feature_values)))
