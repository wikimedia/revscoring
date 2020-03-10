
from pytest import mark

from revscoring.features import Feature
from revscoring.scoring.models.model import Classifier, Learned, Model


def test_model():
    m = Model([Feature("foo", returns=int)], version="0.0.1")

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
    model = Learned([Feature("foo", returns=int)])
    assert model.trained is None


def test_classifier():
    model = Classifier([Feature("foo", returns=int)], [True, False])
    assert 'statustics' not in model.info
