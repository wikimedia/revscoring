"""
A collection of Naive Bayes type classifier models.

.. autoclass:: revscoring.scorer_models.GaussianNB
    :members:
    :member-order:

.. autoclass:: revscoring.scorer_models.MultinomialNB
    :members:
    :member-order:

.. autoclass:: revscoring.scorer_models.BernoulliNB
    :members:
    :member-order:
"""
import logging

from sklearn import naive_bayes

from .sklearn_classifier import ScikitLearnClassifier

logger = logging.getLogger(__name__)


class NB(ScikitLearnClassifier):
    def __init__(self, features, *, version=None, nb=None,
                 sklearn_class=None, balanced_sample=False,
                 balanced_sample_weight=False,
                 scale=False, center=False, test_statistics=None, **kwargs):
        if nb is None:
            nb = sklearn_class(**kwargs)
        super().__init__(features, classifier_model=nb, version=version,
                         balanced_sample=balanced_sample,
                         balanced_sample_weight=balanced_sample_weight,
                         scale=scale, center=center,
                         test_statistics=test_statistics)


class GaussianNB(NB):
    """
    Implements a Gaussian Naive Bayes model.

    :Params:
        features : `list` ( :class:`revscoring.Feature` )
            The features that the model will be trained on
        version : str
            A version string representing the version of the model
        `**kwargs`
            Passed to :class:`sklearn.naive_bayes.GaussianNB`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, sklearn_class=naive_bayes.GaussianNB, **kwargs)


class MultinomialNB(NB):
    """
    Implements a Multinomial Naive Bayes model.

    :Params:
        features : `list` ( :class:`revscoring.Feature` )
            The features that the model will be trained on
        version : str
            A version string representing the version of the model
        `**kwargs`
            Passed to :class:`sklearn.naive_bayes.MultinomialNB`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, sklearn_class=naive_bayes.MultinomialNB,
                         **kwargs)


class BernoulliNB(NB):
    """
    Implements a Bernoulli Naive Bayes model.

    :Params:
        features : `list` ( :class:`revscoring.Feature` )
            The features that the model will be trained on
        version : str
            A version string representing the version of the model
        `**kwargs`
            Passed to :class:`sklearn.naive_bayes.BernoulliNB`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, sklearn_class=naive_bayes.BernoulliNB,
                         **kwargs)
