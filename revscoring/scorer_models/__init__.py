"""
This module contains a collection of models that implement a simple function:
:func:`~revscoring.scorer_models.ScorerModel.score`.  Currently, all models are
a subclass of :class:`~revscoring.scorer_models.scorer_model.MLScorerModel`
which means that they also implement
:meth:`~revscoring.scorer_models.scorer_model.MLScorerModel.train` and
:meth:`~revscoring.scorer_models.scorer_model.MLScorerModel.test` methods.

svc
+++
.. automodule:: revscoring.scorer_models.svc

nb
++
.. automodule:: revscoring.scorer_models.nb

rf
++
.. automodule:: revscoring.scorer_models.rf

scorer_model
++++++++++++
.. automodule:: revscoring.scorer_models.scorer_model


"""
from .svc import SVC, SVCModel, LinearSVC, LinearSVCModel, RBFSVC, RBFSVCModel
from .nb import (NB, NBModel, GaussianNB, GaussianNBModel, MultinomialNB,
                 MultinomialNBModel, BernoulliNB, BernoulliNBModel)
from .scorer_model import ScorerModel, MLScorerModel, ScikitLearnClassifier
from .rf import RF, RFModel

__all__ = [
    SVC, SVCModel, LinearSVC, LinearSVCModel, RBFSVC, RBFSVCModel,
    NB, NBModel, GaussianNB, GaussianNBModel, MultinomialNB,
    MultinomialNBModel, BernoulliNB, BernoulliNBModel,
    ScorerModel, MLScorerModel, ScikitLearnClassifier,
    RF, RFModel
]
