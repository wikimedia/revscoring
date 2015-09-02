"""
.. autoclass:: revscoring.scorer_models.nb.GaussianNB
    :members:
    :member-order:

.. autoclass:: revscoring.scorer_models.nb.MultinomialNB
    :members:
    :member-order:

.. autoclass:: revscoring.scorer_models.nb.BernoulliNB
    :members:
    :member-order:
"""
import logging

from sklearn import naive_bayes

from .scorer_model import ScikitLearnClassifier

logger = logging.getLogger("revscoring.scorers.nb")


class NB(ScikitLearnClassifier):
    def __init__(self, features, *, version=None, nb=None,
                 sklearn_class=None, **kwargs):
        if nb is None:
            nb = sklearn_class(**kwargs)
        super().__init__(features, classifier_model=nb, version=version)
NBModel = NB
"Alias for backwards compatibility"


class GaussianNB(NBModel):
    """
    Implements a Gaussian Naive Bayes model.

    :Params:
        features : `collection` of :class:`~revscoring.features.Feature`
            The features that the model will be trained on
        version : str
            A version string representing the version of the model
        `**kwargs`
            Passed to :class:`sklearn.naive_bayes.GaussianNB`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, sklearn_class=naive_bayes.GaussianNB, **kwargs)
GaussianNBModel = GaussianNB
"Alias for backwards compatibility"


class MultinomialNB(NBModel):
    """
    Implements a Multinomial Naive Bayes model.

    :Params:
        features : `collection` of :class:`~revscoring.features.Feature`
            The features that the model will be trained on
        version : str
            A version string representing the version of the model
        `**kwargs`
            Passed to :class:`sklearn.naive_bayes.MultinomialNB`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, sklearn_class=naive_bayes.MultinomialNB,
                         **kwargs)
MultinomialNBModel = MultinomialNB
"Alias for backwards compatibility"


class BernoulliNB(NBModel):
    """
    Implements a Bernoulli Naive Bayes model.

    :Params:
        features : `collection` of :class:`~revscoring.features.Feature`
            The features that the model will be trained on
        version : str
            A version string representing the version of the model
        `**kwargs`
            Passed to :class:`sklearn.naive_bayes.BernoulliNB`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, sklearn_class=naive_bayes.BernoulliNB,
                         **kwargs)
BernoulliNBModel = BernoulliNB
"Alias for backwards compatibility"
