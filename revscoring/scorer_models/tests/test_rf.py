from ..rf import RF
from ..scorer_model import ScorerModel
from .util import (FEATURES, get_and_format_info, pickle_and_unpickle,
                   train_score)


def test_rf():
    model = RF(FEATURES)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scorer_models.RF",
                'features': [1, 2, 3]
            }
        }
    }
    model = ScorerModel.from_config(config, 'test')
    assert isinstance(model, RF)
