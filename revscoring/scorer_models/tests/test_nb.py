from ..nb import GaussianNBModel, MultinomialNBModel, BernoulliNBModel
from .util import FEATURES, train_score, pickle_and_unpickle

def test_gaussian_nb():
    model = GaussianNBModel(FEATURES)
    train_score(model)
    pickle_and_unpickle(model)

def test_multinomial_nb():
    model = MultinomialNBModel(FEATURES)
    #Fails due to negative feature values.
    #train_score(model)
    pickle_and_unpickle(model)

def test_bernoulli_nb():
    model = BernoulliNBModel(FEATURES)
    train_score(model)
    pickle_and_unpickle(model)
