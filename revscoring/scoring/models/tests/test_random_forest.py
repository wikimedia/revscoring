from ..model import Model
from ..random_forest import RandomForest
from .util import FEATURES, format_info, pickle_and_unpickle, train_test


def test_random_forest():
    model = RandomForest(FEATURES)
    format_info(model)
    train_test(model)
    pickle_and_unpickle(model)
    format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scoring.models.RandomForest",
                'features': [1, 2, 3]
            }
        }
    }
    model = Model.from_config(config, 'test')
    assert isinstance(model, RandomForest)
