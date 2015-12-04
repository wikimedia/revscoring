from nose.tools import eq_

from ...features import Feature
from ..scorer_model import ScorerModel


def test_scorer_model():
    sm = ScorerModel([Feature("foo")], version="0.0.1")

    eq_(sm.version, "0.0.1")
