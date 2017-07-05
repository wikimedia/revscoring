"""
A collection of Naive Bayes type classifier models.

.. autoclass:: revscoring.scoring.models.GaussianNB
    :members:
    :member-order:

.. autoclass:: revscoring.scoring.models.MultinomialNB
    :members:
    :member-order:

.. autoclass:: revscoring.scoring.models.BernoulliNB
    :members:
    :member-order:
"""
import logging

from sklearn import naive_bayes

from .sklearn import ProbabilityClassifier

logger = logging.getLogger(__name__)


class NaiveBayes(ProbabilityClassifier):
    pass


class GaussianNB(NaiveBayes):
    """
    Implements a Gaussian Naive Bayes model
    """
    Estimator = naive_bayes.GaussianNB


class MultinomialNB(NaiveBayes):
    """
    Implements a Multinomial Naive Bayes model
    """
    Estimator = naive_bayes.MultinomialNB


class BernoulliNB(NaiveBayes):
    """
    Implements a Bernoulli Naive Bayes model
    """
    Estimator = naive_bayes.BernoulliNB
