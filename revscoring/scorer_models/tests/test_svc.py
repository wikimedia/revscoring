from ..scorer_model import ScorerModel
from ..svc import RBFSVC, SVC, LinearSVC
from .util import (FEATURES, get_and_format_info, pickle_and_unpickle,
                   train_score)


def test_svc():
    model = SVC(FEATURES)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)

    model = SVC(FEATURES, scale=True, center=True, balanced_sample=True)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scorer_models.SVC",
                'features': [1, 2, 3]
            }
        }
    }
    model = ScorerModel.from_config(config, 'test')
    assert isinstance(model, SVC)


def test_linear_svc():
    model = LinearSVC(FEATURES)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scorer_models.LinearSVC",
                'features': [1, 2, 3]
            }
        }
    }
    model = ScorerModel.from_config(config, 'test')
    assert isinstance(model, LinearSVC)


def test_rbf_svc():
    model = RBFSVC(FEATURES)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scorer_models.RBFSVC",
                'features': [1, 2, 3]
            }
        }
    }
    model = ScorerModel.from_config(config, 'test')
    assert isinstance(model, RBFSVC)
