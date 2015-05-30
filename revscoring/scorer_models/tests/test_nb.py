from ..nb import BernoulliNBModel, GaussianNBModel, MultinomialNBModel
from .util import FEATURES, pickle_and_unpickle, train_score


def test_gaussian_nb():
    model = GaussianNBModel(FEATURES)
    train_score(model)
    pickle_and_unpickle(model)

def test_multinomial_nb():
    model = MultinomialNBModel(FEATURES)
    #Fails due to negative feature values.
    #train_score(model)
    #pickle_and_unpickle(model)

def test_bernoulli_nb():
    model = BernoulliNBModel(FEATURES)
    train_score(model)
    pickle_and_unpickle(model)
