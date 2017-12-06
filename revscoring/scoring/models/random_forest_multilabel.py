"""
A collection of Random Forest type classifier models for multilabel.

.. autoclass:: revscoring.scoring.models.RandomForestMultilabel
    :members:
    :member-order:
"""
import logging

from sklearn.ensemble import RandomForestClassifier

from .sklearn import MultilabelClassifier

logger = logging.getLogger(__name__)


class RandomForestMultilabel(MultilabelClassifier):
    """
    Implements a Random Forest model.
    """
    Estimator = RandomForestClassifier

