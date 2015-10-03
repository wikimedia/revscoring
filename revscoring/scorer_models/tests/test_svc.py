from ..svc import LinearSVCModel, RBFSVCModel, SVCModel
from .util import (FEATURES, get_and_format_info, pickle_and_unpickle,
                   train_score)


def test_svc():
    model = SVCModel(FEATURES)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)


def test_linear_svc():
    model = LinearSVCModel(FEATURES)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)


def test_rbf_svc():
    model = RBFSVCModel(FEATURES)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)
