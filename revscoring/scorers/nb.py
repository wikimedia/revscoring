from sklearn import naive_bayes

from .scorer import ScikitLearnClassifier

import logging

logger = logging.getLogger("revscoring.scorers.nb")

class NBModel(ScikitLearnClassifier):    
    def __init__(self, features, *, 
                       language=None, nb=None, sklearn_class=None, **kwargs):
        if nb is None: nb = sklearn_class(**kwargs)
        super().__init__(features, classifier_model=nb, language=language)

class GaussianNBModel(NBModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, sklearn_class=naive_bayes.GaussianNB, **kwargs)
    
class MultinomialNBModel(NBModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, sklearn_class=naive_bayes.MultinomialNB, **kwargs)

class BernoulliNBModel(NBModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, sklearn_class=naive_bayes.BernoulliNB, **kwargs)
