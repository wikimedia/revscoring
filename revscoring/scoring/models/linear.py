"""
A collection of linear classifier models.

.. autoclass:: revscoring.scoring.models.LogisticRegression
    :members:
    :member-order:
"""
import logging

from sklearn.linear_model import LogisticRegression as sklearn_LR

from .sklearn import ProbabilityClassifier

logger = logging.getLogger(__name__)


class LogisticRegression(ProbabilityClassifier):
    """
    Implements a Logistic Regression
    """
    Estimator = sklearn_LR
