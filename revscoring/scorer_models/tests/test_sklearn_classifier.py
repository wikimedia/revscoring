from nose.tools import eq_, raises

from ...features import Feature
from ..sklearn_classifier import ScikitLearnClassifier
from ..test_statistics import table


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


class FakeIdentityClassifier(ScikitLearnClassifier):
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
    table_statistic = table()

    # Ensures that one call executes in the local process
    skc._generate_test_stats((0, cv_feature_values[:5], cv_feature_values[5:],
                              [table_statistic]))
    test_stats = skc.cross_validate(cv_feature_values,
                                    test_statistics=[table_statistic])

    assert 'cross-validation' in test_stats
    eq_(test_stats[table_statistic],
        {True: {True: 5},
         False: {False: 5}})

    assert 'table' in skc.format_info(format="json")['test_stats']


@raises(ValueError)
def test_sklearn_format_error():
    skc = FakeIdentityClassifier(
        [Feature("foo")], version="0.0.1")
    skc.format_info(format="foo")
