"""
This module contains a collection of models that implement a simple function:
:func:`~revscoring.ScorerModel.score`.  Currently, all models are
a subclass of :class:`revscoring.scorer_models.MLScorerModel`
which means that they also implement
:meth:`~revscoring.scorer_models.MLScorerModel.train` and
:meth:`~revscoring.scorer_models.MLScorerModel.test` methods.  See
:mod:`revscoring.scorer_models.statistics` for stats that can be applied to
models.



Support Vector Classifiers
++++++++++++++++++++++++++
.. automodule:: revscoring.scorer_models.svc

Naive Bayes Classifiers
+++++++++++++++++++++++
.. automodule:: revscoring.scorer_models.nb

Random Forest
+++++++++++++
.. automodule:: revscoring.scorer_models.rf

Gradient Boosting
+++++++++++++++++
.. automodule:: revscoring.scorer_models.gradient_boosting

Abstract classes
++++++++++++++++
.. automodule:: revscoring.scorer_models.scorer_model

"""
from .svc import SVC, LinearSVC, RBFSVC
from .gradient_boosting import GradientBoosting
from .nb import NB, GaussianNB, MultinomialNB, BernoulliNB
from .scorer_model import ScorerModel, MLScorerModel
from .sklearn_classifier import ScikitLearnClassifier
from .rf import RF

__all__ = [
    SVC, LinearSVC, RBFSVC, NB, GaussianNB, MultinomialNB, BernoulliNB,
    ScorerModel, MLScorerModel, ScikitLearnClassifier, RF, GradientBoosting
]
