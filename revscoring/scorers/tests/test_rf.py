from ..rf import RFModel
from .util import FEATURES, pickle_and_unpickle, train_score


def test_rf():
    model = RFModel(FEATURES)
    train_score(model)
    pickle_and_unpickle(model)
