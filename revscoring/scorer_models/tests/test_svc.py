from ..svc import RBFSVC, SVC, LinearSVC
from .util import (FEATURES, get_and_format_info, pickle_and_unpickle,
                   train_score)


def test_svc():
    model = SVC(FEATURES)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)


def test_linear_svc():
    model = LinearSVC(FEATURES)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)


def test_rbf_svc():
    model = RBFSVC(FEATURES)
    get_and_format_info(model)
    train_score(model)
    pickle_and_unpickle(model)
    get_and_format_info(model)
