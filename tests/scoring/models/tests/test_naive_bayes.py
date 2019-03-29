from revscoring.scoring.models.model import Model
from revscoring.scoring.models.naive_bayes import (BernoulliNB, GaussianNB,
                                                   MultinomialNB)

from .util import FEATURES, format_info, pickle_and_unpickle, train_test


def test_gaussian_nb():
    model = GaussianNB(FEATURES, [True, False])
    format_info(model)
    train_test(model)
    reconstructed_model = pickle_and_unpickle(model)
    train_test(reconstructed_model)
    format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scoring.models.GaussianNB",
                'labels': [True, False],
                'features': [1, 2, 3]
            }
        }
    }
    model = Model.from_config(config, 'test')
    assert isinstance(model, GaussianNB)


def test_multinomial_nb():
    model = MultinomialNB(FEATURES, [True, False])
    format_info(model)

    # Fails due to negative feature values.
    # train_score(model)
    # pickle_and_unpickle(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scoring.models.MultinomialNB",
                'labels': [True, False],
                'features': [1, 2, 3]
            }
        }
    }
    model = Model.from_config(config, 'test')
    assert isinstance(model, MultinomialNB)


def test_bernoulli_nb():
    model = BernoulliNB(FEATURES, [True, False])
    format_info(model)
    train_test(model)
    reconstructed_model = pickle_and_unpickle(model)
    train_test(reconstructed_model)
    format_info(model)

    config = {
        'scorer_models': {
            'test': {
                'class': "revscoring.scoring.models.BernoulliNB",
                'labels': [True, False],
                'features': [1, 2, 3]
            }
        }
    }
    model = Model.from_config(config, 'test')
    assert isinstance(model, BernoulliNB)
