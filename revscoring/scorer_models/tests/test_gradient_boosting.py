from ..gradient_boosting import GradientBoosting
from ..scorer_model import ScorerModel
from .util import (FEATURES, get_and_format_info, pickle_and_unpickle,
                   train_score)


def test_gb():
    model = GradientBoosting(FEATURES)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scorer_models.GradientBoosting",
                'features': [1, 2, 3]
            }
        }
    }
    model = ScorerModel.from_config(config, 'test')
    assert isinstance(model, GradientBoosting)
