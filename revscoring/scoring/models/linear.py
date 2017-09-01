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

    def __init__(self, *args, label_weights=None, **kwargs):
        if label_weights:
            logger.warn("LogisticRegression does not support label_weights.")
        super().__init__(*args, **kwargs)
