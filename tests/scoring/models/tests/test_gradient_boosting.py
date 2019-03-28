from revscoring.scoring.models.gradient_boosting import GradientBoosting
from revscoring.scoring.models.model import Model

from .util import (FEATURES, format_info, pickle_and_unpickle, train_test,
                   train_test_multilabel)


def test_gradient_boosting():
    model = GradientBoosting(FEATURES, [True, False])
    format_info(model)
    train_test(model)
    reconstructed_model = pickle_and_unpickle(model)
    train_test(reconstructed_model)
    format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scoring.models.GradientBoosting",
                'labels': [True, False],
                'features': [1, 2, 3]
            }
        }
    }
    model = Model.from_config(config, 'test')
    assert isinstance(model, GradientBoosting)


def test_gradient_boosting_multilabel():
    model = GradientBoosting(FEATURES, ["A", "B", "C"], multilabel=True)
    format_info(model)
    train_test_multilabel(model)
    reconstructed_model = pickle_and_unpickle(model)
    train_test_multilabel(reconstructed_model)
    format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scoring.models.GradientBoosting",
                'labels': ["A", "B", "C"],
                'features': [1, 2, 3]
            }
        }
    }
    model = Model.from_config(config, 'test')
    assert isinstance(model, GradientBoosting)
