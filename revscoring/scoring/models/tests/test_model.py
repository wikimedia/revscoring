from nose.tools import eq_

from ....features import Feature
from ..model import Classifier, LearnedModel, Model, ThresholdClassifier


def test_model():
    m = Model([Feature("foo")], version="0.0.1")

    eq_(m.version, "0.0.1")


def test_from_config():
    config = {
        'scorer_models': {
            'test': {
                'module': "nose.tools.eq_"
            }
        }
    }
    model = Model.from_config(config, 'test')
    eq_(model, eq_)


def test_learned_model():
    model = LearnedModel([Feature("foo")])
    eq_(model.trained, None)


def test_classifier():
    model = Classifier([Feature("foo")])
    assert model.statistics is not NotImplemented


def test_threshold_classifier():
    model = ThresholdClassifier([Feature("foo")])
    assert model.statistics is not NotImplemented
