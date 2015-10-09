from .feature import Constant, Feature, Modifier


def trim(features, context=None):
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
            cache.add(feature)
            yield feature
