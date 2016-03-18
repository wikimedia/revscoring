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

    :Params:
        features : `list` ( :class:`revscoring.Feature` )
            The features that the model will be trained on
        version : str
            A version string representing the version of the model
        `**kwargs`
            Passed to :class:`sklearn.svm.SVC`
    """
    def __init__(self, features, version=None, svc=None,
                 balanced_sample=False, balanced_sample_weight=False,
                 scale=False, center=False, test_statistics=None, **kwargs):
        if svc is None:
            classifier_model = svm.SVC(probability=True, **kwargs)
        else:
            classifier_model = svc

        super().__init__(features, classifier_model, version=version,
                         balanced_sample=balanced_sample,
                         balanced_sample_weight=balanced_sample_weight,
                         scale=scale, center=center,
                         test_statistics=test_statistics)

        self.feature_stats = None
        self.weights = None


class LinearSVC(SVC):
    """
    Implements a Support Vector Classifier model with a Linear kernel.

    :Params:
        features : `list` ( :class:`revscoring.Feature` )
            The features that the model will be trained on
        version : str
            A version string representing the version of the model
        `**kwargs`
            Passed to :class:`sklearn.svm.SVC`
    """
    def __init__(self, *args, **kwargs):
        if 'kernel' in kwargs:
            raise TypeError("'kernel' is hard-coded to 'linear'. If you'd " +
                            "like to use a different kernel, use SVCModel.")
        super().__init__(*args, kernel="linear", **kwargs)


class RBFSVC(SVC):
    """
    Implements a Support Vector Classifier model with an RBF kernel.

    :Params:
        features : `list` ( :class:`revscoring.Feature` )
            The features that the model will be trained on
        version : str
            A version string representing the version of the model
        `**kwargs`
            Passed to :class:`sklearn.svm.SVC`
    """
    def __init__(self, *args, **kwargs):
        if 'kernel' in kwargs:
            raise TypeError("'kernel' is hard-coded to 'rbf'. If you'd " +
                            "like to use a different kernel, try SVCModel.")
        super().__init__(*args, kernel="rbf", **kwargs)
