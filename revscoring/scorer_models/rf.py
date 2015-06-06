"""
.. autoclass:: revscoring.scorer_models.rf.RF
    :members:
    :member-order:
"""
import logging

from sklearn.ensemble import RandomForestClassifier

from .scorer_model import ScikitLearnClassifier

logger = logging.getLogger("revscoring.scorers.rf")

class RF(ScikitLearnClassifier):
    """
    Implements a Random Forest model.

    :Params:
        features : `collection` of :class:`~revscoring.features.feature.Feature`
            The features that the model will be trained on
        language : :class:`~revscoring.languages.language.Language`
            The language context applied when extracting features.
        version : str
            A version string representing the version of the model
        `**kwargs`
            Passed to :class:`sklearn.ensemble.RandomForestClassifier`
    """
    def __init__(self, features, *, language=None, version=None, rf=None, **kwargs):

        if rf is None: rf = RandomForestClassifier(**kwargs)

        super().__init__(features, classifier_model=rf, language=language,
                         version=version)
RFModel = RF
"Alias for backwards compatibility"
