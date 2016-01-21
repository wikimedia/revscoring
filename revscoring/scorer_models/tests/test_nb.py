from ..nb import BernoulliNB, GaussianNB, MultinomialNB
from ..scorer_model import ScorerModel
from .util import (FEATURES, get_and_format_info, pickle_and_unpickle,
                   train_score)


def test_gaussian_nb():
    model = GaussianNB(FEATURES)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scorer_models.GaussianNB",
                'features': [1, 2, 3]
            }
        }
    }
    model = ScorerModel.from_config(config, 'test')
    assert isinstance(model, GaussianNB)


def test_multinomial_nb():
    model = MultinomialNB(FEATURES)
    get_and_format_info(model)

    # Fails due to negative feature values.
    # train_score(model)
    # pickle_and_unpickle(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scorer_models.MultinomialNB",
                'features': [1, 2, 3]
            }
        }
    }
    model = ScorerModel.from_config(config, 'test')
    assert isinstance(model, MultinomialNB)


def test_bernoulli_nb():
    model = BernoulliNB(FEATURES)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scorer_models.BernoulliNB",
                'features': [1, 2, 3]
            }
        }
    }
    model = ScorerModel.from_config(config, 'test')
    assert isinstance(model, BernoulliNB)
