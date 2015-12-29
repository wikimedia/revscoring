from ..nb import BernoulliNB, GaussianNB, MultinomialNB
from .util import (FEATURES, get_and_format_info, pickle_and_unpickle,
                   train_score)


def test_gaussian_nb():
    model = GaussianNB(FEATURES)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)


def test_multinomial_nb():
    model = MultinomialNB(FEATURES)
    get_and_format_info(model)

    # Fails due to negative feature values.
    # train_score(model)
    # pickle_and_unpickle(model)


def test_bernoulli_nb():
    model = BernoulliNB(FEATURES)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)
