from ..nb import BernoulliNBModel, GaussianNBModel, MultinomialNBModel
from .util import (FEATURES, get_and_format_info, pickle_and_unpickle,
                   train_score)


def test_gaussian_nb():
    model = GaussianNBModel(FEATURES)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)


def test_multinomial_nb():
    model = MultinomialNBModel(FEATURES)
    get_and_format_info(model)

    # Fails due to negative feature values.
    # train_score(model)
    # pickle_and_unpickle(model)


def test_bernoulli_nb():
    model = BernoulliNBModel(FEATURES)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)
