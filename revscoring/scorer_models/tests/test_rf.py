from ..rf import RFModel
from .util import (FEATURES, get_and_format_info, pickle_and_unpickle,
                   train_score)


def test_rf():
    model = RFModel(FEATURES)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)
