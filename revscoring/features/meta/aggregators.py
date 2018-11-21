"""
These Meta-Features apply an aggregate function to
:class:`~revscoring.Datasource` that return lists of values.

.. autoclass revscoring.features.meta.aggregators.sum

.. autoclass revscoring.features.meta.aggregators.len

.. autoclass revscoring.features.meta.aggregators.max

.. autoclass revscoring.features.meta.aggregators.min
"""
import statistics

import numpy as np

from ..feature import Feature
from ..feature_vector import FeatureVector

len_builtin = len
sum_builtin = sum
max_builtin = max
min_builtin = min
mean_builtin = statistics.mean


class AggregatorsScalar(Feature):
    def __init__(self, items_datasource, func, name=None, returns=float):
        name = self._format_name(
            name, [items_datasource], func_name=func.__name__)
        super().__init__(name, self.process, depends_on=[items_datasource],
                         returns=returns)
        self.func = func

    def process(self, items):
        if items is None or len_builtin(items) == 0:
            return self.returns()
        else:
            return self.returns(self.func(items))


class AggregatorsVector(FeatureVector):
    def __init__(self, items_datasource, func, name=None, returns=float):
        name = self._format_name(
            name, [items_datasource], func_name=func.__name__)
        super().__init__(name, self.process, depends_on=[items_datasource],
                         returns=returns)
        self.func = func

    def process(self, items):
        if len_builtin(items) == 0 or items[0] is None or \
                len_builtin(items[0]) == 0:
            return [self.returns()]
        else:
            return_func = np.vectorize(self.returns)
            # apply the function over each row
            return return_func(np.apply_along_axis(
                self.func, 0, np.array(items, dtype=self.returns))).tolist()


def aggregators_factory(func):
    def wrapper(items_datasource, name=None, returns=float, vector=False):
        func_tocall = func(items_datasource, name, returns)
        if vector:
            return AggregatorsVector(
                items_datasource, func_tocall, name, returns)
        else:
            return AggregatorsScalar(
                items_datasource, func_tocall, name, returns)
    return wrapper


@aggregators_factory
def sum(items_datasource, name=None, returns=float, vector=False):
    return sum_builtin


@aggregators_factory
def len(items_datasource, name=None, returns=int, vector=False):
    return len_builtin


@aggregators_factory
def max(items_datasource, name=None, returns=float, vector=False):
    return max_builtin


@aggregators_factory
def min(items_datasource, name=None, returns=float, vector=False):
    return min_builtin


@aggregators_factory
def mean(items_datasource, name=None, returns=np.float64, vector=False):
    return mean_builtin
