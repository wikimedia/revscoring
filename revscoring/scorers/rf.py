import logging

from sklearn.ensemble import RandomForestClassifier

from .scorer import ScikitLearnClassifier

logger = logging.getLogger("revscoring.scorers.rf")

class RFModel(ScikitLearnClassifier):

    def __init__(self, features, *, language=None, rf=None, **kwargs):

        if rf is None: rf = RandomForestClassifier(**kwargs)

        super().__init__(features, classifier_model=rf, language=language)
