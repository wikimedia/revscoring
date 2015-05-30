import logging

from sklearn import naive_bayes

from .scorer_model import ScikitLearnClassifier

logger = logging.getLogger("revscoring.scorers.nb")

class NBModel(ScikitLearnClassifier):
    def __init__(self, features, *, language=None, version=None, nb=None,
                       sklearn_class=None, **kwargs):
        if nb is None: nb = sklearn_class(**kwargs)
        super().__init__(features, classifier_model=nb, language=language,
                         version=version)

class GaussianNBModel(NBModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, sklearn_class=naive_bayes.GaussianNB, **kwargs)

class MultinomialNBModel(NBModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, sklearn_class=naive_bayes.MultinomialNB, **kwargs)

class BernoulliNBModel(NBModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, sklearn_class=naive_bayes.BernoulliNB, **kwargs)
