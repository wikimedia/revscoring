from ..model import Model
from ..svc import RBFSVC, SVC, LinearSVC
from .util import FEATURES, format_info, pickle_and_unpickle, train_test


def test_svc():
    model = SVC(FEATURES, [True, False])
    format_info(model)
    train_test(model)
    pickle_and_unpickle(model)
    format_info(model)

    model = SVC(FEATURES, [True, False], scale=True, center=True)
    format_info(model)
    train_test(model)
    pickle_and_unpickle(model)
    format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scoring.models.SVC",
                'labels': [True, False],
                'features': [1, 2, 3]
            }
        }
    }
    model = Model.from_config(config, 'test')
    assert isinstance(model, SVC)


def test_linear_svc():
    model = LinearSVC(FEATURES, [True, False])
    format_info(model)
    train_test(model)
    pickle_and_unpickle(model)
    format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scoring.models.LinearSVC",
                'labels': [True, False],
                'features': [1, 2, 3]
            }
        }
    }
    model = Model.from_config(config, 'test')
    assert isinstance(model, LinearSVC)


def test_rbf_svc():
    model = RBFSVC(FEATURES, [True, False])
    format_info(model)
    train_test(model)
    pickle_and_unpickle(model)
    format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scoring.models.RBFSVC",
                'labels': [True, False],
                'features': [1, 2, 3]
            }
        }
    }
    model = Model.from_config(config, 'test')
    assert isinstance(model, RBFSVC)
