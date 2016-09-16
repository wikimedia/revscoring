"""
A collection of Support Vector Machine type classifier models.

.. autoclass:: revscoring.scorer_models.LinearSVC
    :members:
    :member-order:

.. autoclass:: revscoring.scorer_models.RBFSVC
    :members:
    :member-order:

.. autoclass:: revscoring.scorer_models.SVC
    :members:
    :member-order:

"""
from sklearn import svm

from .sklearn_classifier import ScikitLearnClassifier


class SVC(ScikitLearnClassifier):
    """
    Implements a Support Vector Classifier model.
    """
    Estimator = svm.SVC
    Base_Params = {'probability': True}


class LinearSVC(SVC):
    """
    Implements a Support Vector Classifier model with a Linear kernel.
    """
    Base_Params = {'probability': True, 'kernel': "linear"}


class RBFSVC(SVC):
    """
    Implements a Support Vector Classifier model with an RBF kernel.
    """
    Base_Params = {'probability': True, 'kernel': "rbf"}
