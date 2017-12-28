from ..random_forest_ovr import RandomForestOneVsRest
from ..model import Model
from .util import (FEATURES, format_info, pickle_and_unpickle,
                   train_test_multilabel)


def test_random_forest_ensemble():
    model = RandomForestOneVsRest(FEATURES, ["A", "B", "C"], multilabel=True)
    format_info(model)
    train_test_multilabel(model)
    reconstructed_model = pickle_and_unpickle(model)
    train_test_multilabel(reconstructed_model)
    format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scoring.models.RandomForestOneVsRest",
                'labels': ["A", "B", "C"],
                'features': [1, 2, 3]
            }
        }
    }
    model = Model.from_config(config, 'test')
    assert isinstance(model, RandomForestOneVsRest)
