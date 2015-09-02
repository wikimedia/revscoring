from ..svc import LinearSVCModel, RBFSVCModel, SVCModel
from .util import FEATURES, pickle_and_unpickle, train_score


def test_svc():
    model = SVCModel(FEATURES)
    train_score(model)
    pickle_and_unpickle(model)


def test_linear_svc():
    model = LinearSVCModel(FEATURES)
    train_score(model)
    pickle_and_unpickle(model)


def test_rbf_svc():
    model = RBFSVCModel(FEATURES)
    train_score(model)
    pickle_and_unpickle(model)
