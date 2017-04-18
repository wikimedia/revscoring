"""
A collection of Random Forest type classifier models.

.. autoclass:: revscoring.scorer_models.RF
    :members:
    :member-order:
"""
import logging

from sklearn.ensemble import RandomForestClassifier

from .sklearn import ProbabilityClassifier

logger = logging.getLogger(__name__)


class RandomForest(ProbabilityClassifier):
    """
    Implements a Random Forest model.
    """
    Estimator = RandomForestClassifier
