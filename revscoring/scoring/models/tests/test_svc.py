from ..model import Model
from ..svc import RBFSVC, SVC, LinearSVC
from .util import FEATURES, format_info, pickle_and_unpickle, train_test


def test_svc():
    model = SVC(FEATURES)
    format_info(model)
    train_test(model)
    pickle_and_unpickle(model)
    format_info(model)

    model = SVC(FEATURES, scale=True, center=True)
    format_info(model)
    train_test(model)
    pickle_and_unpickle(model)
    format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scoring.models.SVC",
                'features': [1, 2, 3]
            }
        }
    }
    model = Model.from_config(config, 'test')
    assert isinstance(model, SVC)


def test_linear_svc():
    model = LinearSVC(FEATURES)
    format_info(model)
    train_test(model)
    pickle_and_unpickle(model)
    format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scoring.models.LinearSVC",
                'features': [1, 2, 3]
            }
        }
    }
    model = Model.from_config(config, 'test')
    assert isinstance(model, LinearSVC)


def test_rbf_svc():
    model = RBFSVC(FEATURES)
    format_info(model)
    train_test(model)
    pickle_and_unpickle(model)
    format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scoring.models.RBFSVC",
                'features': [1, 2, 3]
            }
        }
    }
    model = Model.from_config(config, 'test')
    assert isinstance(model, RBFSVC)
