"""
A collection of Gradient Boosting type classifier models.

.. autoclass:: revscoring.scorer_models.GradientBoosting
    :members:
    :member-order:
"""
import logging

from sklearn.ensemble import GradientBoostingClassifier

from .sklearn import ProbabilityClassifier

logger = logging.getLogger(__name__)


class GradientBoosting(ProbabilityClassifier):
    """
    Implements a Gradient Boosting model.
    """
    Estimator = GradientBoostingClassifier
