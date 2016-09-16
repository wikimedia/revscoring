from collections import namedtuple

from nose.tools import eq_

from ...features import Feature
from ..sklearn_classifier import ScikitLearnClassifier

FakeEstimator = namedtuple("FakeEstimator", 'get_params')


def test_sklean_classifier():
    skc = ScikitLearnClassifier(
        [Feature("foo")], estimator=FakeEstimator(lambda: {}),
        version="0.0.1")

    eq_(skc.version, "0.0.1")
