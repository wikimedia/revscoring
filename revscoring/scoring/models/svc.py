"""
A collection of Support Vector Machine type classifier models.

.. autoclass:: revscoring.scoring.models.LinearSVC
    :members:
    :member-order:

.. autoclass:: revscoring.scoring.models.RBFSVC
    :members:
    :member-order:

.. autoclass:: revscoring.scoring.models.SVC
    :members:
    :member-order:

"""
from sklearn import svm

from .sklearn import ProbabilityClassifier


class SVC(ProbabilityClassifier):
    """
    Implements a Support Vector Classifier model.
    """
    Estimator = svm.SVC
    BASE_PARAMS = {'probability': True}


class LinearSVC(SVC):
    """
    Implements a Support Vector Classifier model with a Linear kernel.
    """
    BASE_PARAMS = {'probability': True, 'kernel': "linear"}


class RBFSVC(SVC):
    """
    Implements a Support Vector Classifier model with an RBF kernel.
    """
    BASE_PARAMS = {'probability': True, 'kernel': "rbf"}
