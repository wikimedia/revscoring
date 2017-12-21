from pytest import raises

from ....features import Feature
from ..sklearn import Classifier, ProbabilityClassifier


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


class FakeIdentityEstimator:

    def __init__(self, *args, **kwargs):
        self.classes_ = [True, False]
        self._params = {}

    def get_params(self):
        return self._params

    def fit(self, vals, labels, sample_weight=None):
        return None

    def predict(self, vals):
        return [v[0] for v in vals]

    def predict_proba(self, vals):
        return [[v[0] * True, 1 - v[0] * True] for v in vals]


class FakeIdentityClassifier(Classifier):
    Estimator = FakeIdentityEstimator


class FakeIdentityProbabilityClassifier(ProbabilityClassifier):
    Estimator = FakeIdentityEstimator


class FakeIdentityClassifierMultilabel(Classifier):
    SUPPORTS_MULTILABEL = True
    SUPPORTS_CLASSWEIGHT = True
    Estimator = FakeIdentityEstimator


def test_sklean_classifier():
    skc = FakeIdentityClassifier(
        [Feature("foo")], [True, False], version="0.0.1")

    assert skc.version == "0.0.1"

    stats = skc.cross_validate(cv_feature_values, folds=2)
    assert (stats['counts']['predictions'] ==
            {True: {False: 0, True: 5},
             False: {False: 5, True: 0}})


def test_sklean_probabilityclassifier():
    skc = FakeIdentityProbabilityClassifier(
        [Feature("foo")], [True, False], version="0.0.1")

    assert skc.version == "0.0.1"

    stats = skc.cross_validate(cv_feature_values, folds=2)
    assert (stats['counts']['predictions'] ==
            {True: {False: 0, True: 5},
             False: {False: 5, True: 0}})


def test_score():
    skc = FakeIdentityClassifier(
        [Feature("foo")], [True, False], version="0.0.1")
    docs = skc.score_many([cv_feature_values[0][0]])
    assert len(docs) == 1

    skc = FakeIdentityProbabilityClassifier(
        [Feature("foo")], [True, False], version="0.0.1")
    docs = skc.score_many([cv_feature_values[0][0]])
    assert len(docs) == 1
    assert 'probability' in docs[0]


def test_score_many():
    skc = FakeIdentityClassifier(
        [Feature("foo")], [True, False], version="0.0.1")
    features, labels = zip(*cv_feature_values)
    docs = skc.score_many(features)
    assert len(docs) == 10

    skc = FakeIdentityProbabilityClassifier(
        [Feature("foo")], [True, False], version="0.0.1")
    features, labels = zip(*cv_feature_values)
    docs = skc.score_many(features)
    assert len(docs) == 10
    assert 'probability' in docs[0]


def test_sklean_classifier_multilabel():
    skc = FakeIdentityClassifierMultilabel(
        [Feature("foo")], [True, False], multilabel=True,
        version="0.0.1", label_weights={True: 5, False: 0.5})
    expected_estimator_params = {'class_weight':
                                 [{0: 1, 1: 5}, {0: 1, 1: 0.5}]}
    assert skc.estimator_params == expected_estimator_params


def test_sklearn_format_error():
    with raises(ValueError):
        skc = FakeIdentityClassifier(
            [Feature("foo")], [True, False], version="0.0.1")
        skc.info.format(formatting="foo")
