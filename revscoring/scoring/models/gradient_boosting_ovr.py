"""
A collection of Gradient Boosting type classifier models,
one for each label in a multilabel setting

.. autoclass:: revscoring.scoring.models.GradientBoostingOneVsRest
    :members:
    :member-order:
"""
import logging

from sklearn.ensemble import GradientBoostingClassifier

from .sklearn import OneVsRestClassifier

logger = logging.getLogger(__name__)


class GradientBoostingOneVsRest(OneVsRestClassifier):
    """
    Implements a One-vs-Rest Random Forest model.
    """
    Estimator = GradientBoostingClassifier
    SUPPORTS_MULTILABEL = True
    SUPPORTS_CLASSWEIGHT = False
