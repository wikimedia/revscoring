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

Linear Regression
+++++++++++++++++
.. automodule:: revscoring.scoring.models.linear

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
from .gradient_boosting import GradientBoosting
from .linear import LogisticRegression
from .model import Classifier, Learned, open_file
from .naive_bayes import BernoulliNB, GaussianNB, MultinomialNB, NaiveBayes
from .random_forest import RandomForest
from .svc import RBFSVC, SVC, LinearSVC

__all__ = [
    Learned, Classifier, open_file,
    SVC, LinearSVC, RBFSVC, NaiveBayes, GaussianNB, MultinomialNB, BernoulliNB,
    RandomForest, GradientBoosting, LogisticRegression
]
