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
    pass


class GaussianNB(NB):
    """
    Implements a Gaussian Naive Bayes model
    """
    Estimator = naive_bayes.GaussianNB


class MultinomialNB(NB):
    """
    Implements a Multinomial Naive Bayes model
    """
    Estimator = naive_bayes.MultinomialNB


class BernoulliNB(NB):
    """
    Implements a Bernoulli Naive Bayes model
    """
    Estimator = naive_bayes.BernoulliNB
