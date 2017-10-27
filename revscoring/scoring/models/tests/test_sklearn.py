from pytest import raises

from ....features import Feature
from ..sklearn import Classifier


class FakeIdentityEstimator:

    def __init__(self):
        self.classes_ = [True, False]
        self._params = {}

    def get_params(self):
        return self._params

    def fit(self, vals, labels, sample_weight=None):
        return None

    def predict(self, vals):
        return [vals[0][0]]

    def predict_proba(self, vals):
        return [[vals[0][0] * True, vals[0][0] * False]]


class FakeIdentityClassifier(Classifier):
    Estimator = FakeIdentityEstimator


def test_sklean_classifier():
    skc = FakeIdentityClassifier(
        [Feature("foo")], [True, False], version="0.0.1")

    assert skc.version == "0.0.1"

    cv_feature_values = [
        ([True], True),
        ([False], False),
        ([True], True),
        ([False], False),
        ([True], True),
        ([False], False),
        ([True], True),
        ([False], False),
        ([True], True),
        ([False], False)
    ]

    stats = skc.cross_validate(cv_feature_values, folds=2)
    assert (stats['counts']['predictions'] ==
            {True: {False: 0, True: 5},
             False: {False: 5, True: 0}})


def test_sklearn_format_error():
    with raises(ValueError):
        skc = FakeIdentityClassifier(
            [Feature("foo")], [True, False], version="0.0.1")
        skc.info.format(formatting="foo")
