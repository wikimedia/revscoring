"""
Statistics represent the fitness of a :class:`revscoring.Model`.  They can
be :func:`~revscoring.scoring.Statistics.fit` to scores and labels and
then output using :func:`~revscoring.scoring.Statistics.format`.  Once
initialize, a :class:`~revscoring.scoring.Statistics` instance behaves like
a `dict` of statistics values.

Classification
++++++++++++++
.. automodule:: revscoring.scoring.statistics.classification

Abstract base class
+++++++++++++++++++
.. automodule:: revscoring.scoring.statistics.statistics

"""
from .classification import Classification

__all__ = [Classification]
