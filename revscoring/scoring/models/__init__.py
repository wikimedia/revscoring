"""
This module contains a collection of models that implement a simple function:
:func:`~revscoring.Model.score`.  Currently, all models are
a subclass of :class:`revscoring.scoring.LearnedModel`
which means that they also implement
:meth:`~revscoring.scorer_models.LearnedModel.train` and
:meth:`~revscoring.Model.test` methods.



Support Vector Classifiers
++++++++++++++++++++++++++
.. automodule:: revscoring.scoring.models.svc

Naive Bayes Classifiers
+++++++++++++++++++++++
.. automodule:: revscoring.scoring.models.naive_bayes

Random Forest
+++++++++++++
.. automodule:: revscoring.scoring.models.random_forest

Gradient Boosting
+++++++++++++++++
.. automodule:: revscoring.scoring.models.gradient_boosting

Abstract classes
++++++++++++++++
.. automodule:: revscoring.scoring.models.model

"""
from .model import LearnedModel, Classifier, ThresholdClassifier
from .svc import SVC, LinearSVC, RBFSVC
from .gradient_boosting import GradientBoosting
from .naive_bayes import NaiveBayes, GaussianNB, MultinomialNB, BernoulliNB
from .random_forest import RandomForest

__all__ = [
    LearnedModel, Classifier, ThresholdClassifier,
    SVC, LinearSVC, RBFSVC, NaiveBayes, GaussianNB, MultinomialNB, BernoulliNB,
    RandomForest, GradientBoosting
]
