"""
A collection of Gradient Boosting type classifier models.

.. autoclass:: revscoring.scorer_models.GradientBoosting
    :members:
    :member-order:
"""
import logging

from sklearn.ensemble import GradientBoostingClassifier

from .sklearn_classifier import ScikitLearnClassifier

logger = logging.getLogger(__name__)


class GradientBoosting(ScikitLearnClassifier):
    """
    Implements a Gradient Boosting model.
    """
    Estimator = GradientBoostingClassifier
