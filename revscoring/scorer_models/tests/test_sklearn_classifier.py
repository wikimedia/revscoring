from nose.tools import eq_

from ...features import Feature
from ..sklearn_classifier import ScikitLearnClassifier


def test_sklean_classifier():
    skc = ScikitLearnClassifier([Feature("foo")], classifier_model=None,
                                version="0.0.1")

    eq_(skc.version, "0.0.1")
