from revscoring.scoring.models.model import Model
from revscoring.scoring.models.random_forest import RandomForest

from .util import (FEATURES, format_info, pickle_and_unpickle, train_test,
                   train_test_multilabel)


def test_random_forest():
    model = RandomForest(FEATURES, [True, False])
    format_info(model)
    train_test(model)
    reconstructed_model = pickle_and_unpickle(model)
    train_test(reconstructed_model)
    format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scoring.models.RandomForest",
                'labels': [True, False],
                'features': [1, 2, 3]
            }
        }
    }
    model = Model.from_config(config, 'test')
    assert isinstance(model, RandomForest)


def test_random_forest_multilabel():
    model = RandomForest(FEATURES, ["A", "B", "C"], multilabel=True)
    format_info(model)
    train_test_multilabel(model)
    reconstructed_model = pickle_and_unpickle(model)
    train_test_multilabel(reconstructed_model)
    format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scoring.models.RandomForest",
                'labels': ["A", "B", "C"],
                'features': [1, 2, 3]
            }
        }
    }
    model = Model.from_config(config, 'test')
    assert isinstance(model, RandomForest)
