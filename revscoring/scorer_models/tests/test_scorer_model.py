from nose.tools import eq_

from ...features import Feature
from ..scorer_model import MLScorerModel, ScorerModel


def test_scorer_model():
    sm = ScorerModel([Feature("foo")], version="0.0.1")

    eq_(sm.version, "0.0.1")

    del sm.version

    eq_(sm.version, None)


def test_from_config():
    config = {
        'scorer_models': {
            'test': {
                'module': "nose.tools.eq_"
            }
        }
    }
    sm = ScorerModel.from_config(config, 'test')
    eq_(sm, eq_)


def test_ml_scorer_model():
    sm = MLScorerModel([Feature("foo")])

    del sm.trained

    eq_(sm.trained, None)
