"""
A collection of Random Forest type classifier models,
one for each label in multilabel setting

.. autoclass:: revscoring.scoring.models.RandomForestOneVsRest
    :members:
    :member-order:
"""
import logging

from sklearn.ensemble import RandomForestClassifier

from .sklearn import OneVsRestClassifier

logger = logging.getLogger(__name__)


class RandomForestOneVsRest(OneVsRestClassifier):
    """
    Implements a One-vs-Rest Random Forest model.
    """
    Estimator = RandomForestClassifier
    SUPPORTS_MULTILABEL = True
    SUPPORTS_CLASSWEIGHT = True
