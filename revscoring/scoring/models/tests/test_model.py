
from ....features import Feature
from ..model import Classifier, Learned, Model

from pytest import mark


def test_model():
    m = Model([Feature("foo")], version="0.0.1")

    assert m.info.lookup('version') == "0.0.1"


def test_from_config():
    config = {
        'scorer_models': {
            'test': {
                'module': "pytest.mark"
            }
        }
    }
    model = Model.from_config(config, 'test')
    assert model == mark


def test_learned_model():
    model = Learned([Feature("foo")])
    assert model.trained is None


def test_classifier():
    model = Classifier([Feature("foo")], [True, False])
    assert 'statustics' not in model.info
