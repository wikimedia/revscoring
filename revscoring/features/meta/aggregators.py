"""
These Meta-Features apply an aggregate function to
:class:`~revscoring.Datasource` that return lists of values.

.. autoclass revscoring.features.meta.aggregators.any

.. autoclass revscoring.features.meta.aggregators.all

.. autoclass revscoring.features.meta.aggregators.sum

.. autoclass revscoring.features.meta.aggregators.len

.. autoclass revscoring.features.meta.aggregators.max

.. autoclass revscoring.features.meta.aggregators.min

.. autoclass revscoring.features.meta.aggregators.mean

.. autoclass revscoring.features.meta.aggregators.first

.. autoclass revscoring.features.meta.aggregators.last
"""
import statistics

from ..feature import Feature, FeatureVector

any_builtin = any
all_builtin = all
len_builtin = len
sum_builtin = sum
max_builtin = max
min_builtin = min


def _first(items):
    return items[0]


def _last(items):
    return items[-1]


class Aggregator:

    def __init__(self, items_datasource, func, name=None, returns=None, empty_default=None):
        name = self._format_name(
            name, [items_datasource], func_name=func.__name__)
        super().__init__(name, self.process, depends_on=[items_datasource],
                         returns=returns)
        self.func = func
        self.empty_default = empty_default


class SingletonAggregator(Aggregator, Feature):

    def process(self, items):
        if items is None or len_builtin(items) == 0:
            if self.empty_default is None:
                raise ValueError(
                    "Cannot generate {0} of {1} -- length of zero"
                    .format(self.func.__name__, self.dependencies[0]))
            else:
                return self.returns(self.empty_default)
        else:
            return self.returns(self.func(items))


class VectorAggregator(Aggregator, FeatureVector):

    def process(self, vectors):
        if vectors is None or len_builtin(vectors) == 0 or \
           vectors[0] is None or len_builtin(vectors[0]) == 0:
            if self.empty_default is None:
                raise ValueError(
                    "Cannot generate {0} of {1} -- length of zero"
                    .format(self.func.__name__, self.dependencies[0]))
            else:
                return [self.returns(self.empty_default)]
        else:
            return [self.returns(self.func(vals)) for vals in zip(*vectors)]


def aggregator(func):
    def wrapper(items_datasource, name=None, returns=None, empty_default=None, vector=False):
        func_tocall, name, returns, empty_default = \
            func(items_datasource, name, returns, empty_default)
        if vector:
            return VectorAggregator(
                items_datasource, func=func_tocall, empty_default=empty_default,
                name=name, returns=returns)
        else:
            return SingletonAggregator(
                items_datasource, func=func_tocall, empty_default=empty_default,
                name=name, returns=returns)
    return wrapper


@aggregator
def all(items_datasource, name, returns, empty_default, vector=False):
    return all_builtin, name, returns or bool, empty_default or False
all.__doc__ = """
Constructs a :class:`revscoring.Feature` that returns True when all items are
also True.

:Parameters:
    items_datasource : :class:`revscoring.Datasource`
        A datasource that returns a collection of items
    name : `str`
        A name for the feature
    returns : `type`
        A type to compare the return of this function to.
    vector : `bool`
        If True, assume that `items_datasource` returns a vector of values.
"""


@aggregator
def any(items_datasource, name, returns, empty_default, vector=False):
    return any_builtin, name, returns or bool, empty_default or False
any.__doc__ = """
Constructs a :class:`revscoring.Feature` that returns True when any items are
also True.

:Parameters:
    items_datasource : :class:`revscoring.Datasource`
        A datasource that returns a collection of items
    name : `str`
        A name for the feature
    returns : `type`
        A type to compare the return of this function to.
    vector : `bool`
        If True, assume that `items_datasource` returns a vector of values.
"""


@aggregator
def sum(items_datasource, name, returns, empty_default, vector=False):
    returns = returns or float
    return sum_builtin, name, returns, empty_default or 0.0
sum.__doc__ = """
Constructs a :class:`revscoring.Feature` that returns the
sum of a collection of items.

:Parameters:
    items_datasource : :class:`revscoring.Datasource`
        A datasource that returns a collection of items
    name : `str`
        A name for the feature
    returns : `type`
        A type to compare the return of this function to.
    vector : `bool`
        If True, assume that `items_datasource` returns a vector of values.
"""


@aggregator
def len(items_datasource, name, returns, empty_default, vector=False):
    return len_builtin, name, int, empty_default or 0
len.__doc__ = """
Constructs a :class:`revscoring.Feature` that returns the length of a
collection of items.

:Parameters:
    items_datasource : :class:`revscoring.Datasource`
        A datasource that returns a collection of items
    name : `str`
        A name for the feature
    returns : `type`
        A type to compare the return of this function to.
    vector : `bool`
        If True, assume that `items_datasource` returns a vector of values.
"""


@aggregator
def mean(items_datasource, name, returns, empty_default, vector=False):
    returns = returns or float
    return statistics.mean, name, returns, empty_default or 0.0
mean.__doc__ = """
Constructs a :class:`revscoring.Feature` that returns the mean of a
collection of items.

:Parameters:
    items_datasource : :class:`revscoring.Datasource`
        A datasource that returns a collection of items
    name : `str`
        A name for the feature
    returns : `type`
        A type to compare the return of this function to.
    vector : `bool`
        If True, assume that `items_datasource` returns a vector of values.
"""


@aggregator
def max(items_datasources, name, returns, empty_default, vector=False):
    return max_builtin, name, returns or float, empty_default or 0
max.__doc__ = """
Constructs a :class:`revscoring.Feature` that returns the maximum of a
collection of items.

:Parameters:
    items_datasource : :class:`revscoring.Datasource`
        A datasource that returns a collection of items
    name : `str`
        A name for the feature
    returns : `type`
        A type to compare the return of this function to.
    vector : `bool`
        If True, assume that `items_datasource` returns a vector of values.
"""


@aggregator
def min(items_datasources, name, returns, empty_default, vector=False):
    return min_builtin, name, returns or float, empty_default or 0
min.__doc__ = """
Constructs a :class:`revscoring.Feature` that returns the minimum of a
collection of items.

:Parameters:
    items_datasource : :class:`revscoring.Datasource`
        A datasource that returns a collection of items
    name : `str`
        A name for the feature
    returns : `type`
        A type to compare the return of this function to.
    vector : `bool`
        If True, assume that `items_datasource` returns a vector of values.
"""


@aggregator
def first(items_datasource, name, returns, empty_default, vector=False):
    return _first, name, returns or float, empty_default or None
first.__doc__ = """
Constructs a :class:`revscoring.Feature` that returns the first of a
collection of items.

:Parameters:
    items_datasource : :class:`revscoring.Datasource`
        A datasource that returns a collection of items
    name : `str`
        A name for the feature
    returns : `type`
        A type to compare the return of this function to.
    vector : `bool`
        If True, assume that `items_datasource` returns a vector of values.
"""


@aggregator
def last(items_datasource, name, returns, empty_default, vector=False):
    return _last, name, returns or float, empty_default or None
last.__doc__ = """
Constructs a :class:`revscoring.Feature` that returns the last of a
collection of items.

:Parameters:
    items_datasource : :class:`revscoring.Datasource`
        A datasource that returns a collection of items
    name : `str`
        A name for the feature
    returns : `type`
        A type to compare the return of this function to.
    vector : `bool`
        If True, assume that `items_datasource` returns a vector of values.
"""
