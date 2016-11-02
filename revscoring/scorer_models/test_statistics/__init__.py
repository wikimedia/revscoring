"""
A collection of statistics generators that can be applied to
:class:`revscoring.ScorerModel`.

.. autoclass:: accuracy

.. autoclass:: precision

.. autoclass:: recall

.. autoclass:: roc

.. autoclass:: precision_recall

.. autoclass:: recall_at_fpr

.. autoclass:: recall_at_precision

.. autoclass:: filter_rate_at_recall

Abstract classes
++++++++++++++++
.. autoclass:: revscoring.scorer_models.test_statistics.TestStatistic
    :members:

.. autoclass:: revscoring.scorer_models.test_statistics.ClassifierStatistic
    :members:
"""
from .test_statistic import TestStatistic, ClassifierStatistic
from .accuracy import accuracy
from .precision import precision
from .recall import recall
from .f1 import f1
from .filter_rate_at_recall import filter_rate_at_recall
from .precision_recall import precision_recall
from .recall_at_fpr import recall_at_fpr
from .recall_at_precision import recall_at_precision
from .roc import roc
from .table import table

__all__ = [TestStatistic, ClassifierStatistic, accuracy, precision, recall, f1,
           filter_rate_at_recall, precision_recall, recall_at_fpr,
           recall_at_precision, roc, table]
