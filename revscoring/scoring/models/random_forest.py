"""
A collection of Random Forest type classifier models.

.. autoclass:: revscoring.scoring.models.RandomForest
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
    SUPPORTS_CLASSWEIGHT = True
