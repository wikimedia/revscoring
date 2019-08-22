from ..aggregators import aggregators_factory


def _first(items):
    return items[0]


def _last(items):
    return items[-1]


@aggregators_factory
def first(items_datasource, name=None, returns=float, vector=False):
    return _first


@aggregators_factory
def last(items_datasource, name=None, returns=float, vector=False):
    return _last
