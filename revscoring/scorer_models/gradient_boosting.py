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

    :Params:
        features : `list` ( :class:`revscoring.Feature` )
            The features that the model will be trained on
        version : str
            A version string representing the version of the model
        `**kwargs`
            Passed to :class:`sklearn.ensemble.GradientBoostingClassifier`
    """
    def __init__(self, features, *, version=None, gb=None,
                 **kwargs):

        if gb is None:
            gb = GradientBoostingClassifier(**kwargs)

        super().__init__(features, classifier_model=gb, version=version)
