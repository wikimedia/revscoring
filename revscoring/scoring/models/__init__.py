"""
This module contains a collection of models that implement a simple function:
:func:`~revscoring.Model.score`.  Currently, all models are
a subclass of :class:`revscoring.scoring.models.Learned`
which means that they also implement
:meth:`~revscoring.scoring.models.Learned.train` and
:meth:`~revscoring.scoring.models.Learned.cross_validate`.

Gradient Boosting
+++++++++++++++++
.. automodule:: revscoring.scoring.models.gradient_boosting

Naive Bayes
+++++++++++
.. automodule:: revscoring.scoring.models.naive_bayes

Support Vector
++++++++++++++
.. automodule:: revscoring.scoring.models.svc

Random Forest
+++++++++++++
.. automodule:: revscoring.scoring.models.random_forest

Abstract classes
++++++++++++++++
.. automodule:: revscoring.scoring.models.model

SciKit Learn-based models
+++++++++++++++++++++++++
.. automodule:: revscoring.scoring.models.sklearn

"""
from .model import Learned, Classifier, ThresholdClassifier
from .svc import SVC, LinearSVC, RBFSVC
from .gradient_boosting import GradientBoosting
from .linear import LogisticRegression
from .naive_bayes import NaiveBayes, GaussianNB, MultinomialNB, BernoulliNB
from .random_forest import RandomForest

__all__ = [
    Learned, Classifier, ThresholdClassifier,
    SVC, LinearSVC, RBFSVC, NaiveBayes, GaussianNB, MultinomialNB, BernoulliNB,
    RandomForest, GradientBoosting, LogisticRegression
]
