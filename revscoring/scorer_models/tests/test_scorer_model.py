from nose.tools import eq_

from ...features import Feature
from ..scorer_model import ScikitLearnClassifier, ScorerModel


def test_scorer_model():
    sm = ScorerModel([Feature("foo")], version="0.0.1")

    eq_(sm.version, "0.0.1")


def test_sklean_classifier():
    skc = ScikitLearnClassifier([Feature("foo")], classifier_model=None,
                                version="0.0.1")

    eq_(skc.version, "0.0.1")
