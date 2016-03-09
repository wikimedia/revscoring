"""
A collection of Random Forest type classifier models.

.. autoclass:: revscoring.scorer_models.RF
    :members:
    :member-order:
"""
import logging

from sklearn.ensemble import RandomForestClassifier

from .sklearn_classifier import ScikitLearnClassifier

logger = logging.getLogger(__name__)


class RF(ScikitLearnClassifier):
    """
    Implements a Random Forest model.

    :Params:
        features : `list` ( :class:`revscoring.Feature` )
            The features that the model will be trained on
        version : str
            A version string representing the version of the model
        `**kwargs`
            Passed to :class:`sklearn.ensemble.RandomForestClassifier`
    """
    def __init__(self, features, *, version=None, rf=None,
                 balanced_sample=False, balanced_sample_weight=False,
                 scale=False, center=False, test_statistics=None, **kwargs):

        if rf is None:
            rf = RandomForestClassifier(**kwargs)

        super().__init__(features, classifier_model=rf, version=version,
                         balanced_sample=balanced_sample,
                         balanced_sample_weight=balanced_sample_weight,
                         scale=scale, center=center,
                         test_statistics=test_statistics)
