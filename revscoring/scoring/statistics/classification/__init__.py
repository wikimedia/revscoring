"""
Classification statistics can be generated for "Classifiers" -- models
that produce factors (aka levels) as an ouput.  E.g. True and False or
"A", "B", or "C".

.. autoclass:: revscoring.scoring.statistics.Classification
    :members:
    :member-order:

.. autoclass:: revscoring.scoring.statistics.classification.Counts
    :members:
    :member-order:

.. autoclass:: revscoring.scoring.statistics.classification.Rates
    :members:
    :member-order:

.. autoclass:: revscoring.scoring.statistics.classification.MicroMacroStats
    :members:
    :member-order:

.. autoclass:: revscoring.scoring.statistics.classification.ScaledPredictionStatistics
    :members:
    :member-order:

.. autoclass:: revscoring.scoring.statistics.classification.ScaledThresholdStatistics
    :members:
    :member-order:

.. autoclass:: revscoring.scoring.statistics.classification.ScaledClassificationMatrix
    :members:
    :member-order:

.. autoclass:: revscoring.scoring.statistics.classification.ThresholdOptimization
    :members:
    :member-order:
"""  # noqa
from .classification import Classification
from .counts import Counts
from .micro_macro_stats import MicroMacroStats
from .rates import Rates
from .scaled_classification_matrix import ScaledClassificationMatrix
from .scaled_prediction_statistics import ScaledPredictionStatistics
from .scaled_threshold_statistics import ScaledThresholdStatistics
from .threshold_optimization import ThresholdOptimization

__all__ = [Classification, Counts, Rates, MicroMacroStats,
           ScaledPredictionStatistics, ScaledThresholdStatistics,
           ScaledClassificationMatrix, ThresholdOptimization]
