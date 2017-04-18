from nose.tools import eq_, raises

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
        [Feature("foo")], version="0.0.1")

    eq_(skc.version, "0.0.1")

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
    eq_(stats['counts']['predictions'],
        {True: {True: 5},
         False: {False: 5}})


@raises(ValueError)
def test_sklearn_format_error():
    skc = FakeIdentityClassifier(
        [Feature("foo")], version="0.0.1")
    skc.format(formatting="foo")
