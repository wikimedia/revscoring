import json
import random
from io import BytesIO
from itertools import chain

from nose.tools import eq_

from ...features import Feature
from ..scorer_model import MLScorerModel


def process_float():
    return float()
some_float = Feature("some_float", process_float(),
                     depends_on=[], returns=float)


def process_other_float():
    return float()
other_float = Feature("other_float", process_other_float(),
                      depends_on=[], returns=float)
FEATURES = [some_float, other_float]


def train_score(model):
    deterministic = random.Random(0)
    observations = list(chain(
        zip(((some, other) for some, other in
             zip((deterministic.normalvariate(1, .3) for i in range(500)),
                 (deterministic.normalvariate(2, .5) for i in range(500)))),
            (False for i in range(500))),
        zip(((some, other) for some, other in
             zip((deterministic.normalvariate(-1, .5) for i in range(50)),
                 (deterministic.normalvariate(-2, .3) for i in range(50)))),
            (True for i in range(50)))
    ))
    deterministic.shuffle(observations)

    mid = int(len(observations)/2)
    train_set = observations[:mid]
    test_set = observations[mid:]

    model.train(train_set)
    score_doc = model.score((-1, -2))

    eq_(score_doc['prediction'], True)
    assert score_doc['probability'][True] > 0.5, \
        "Probability of True {0} is not > 0.5" \
        .format(score_doc['probability'][True])
    json.dumps(score_doc)  # Checks if the doc is JSONable

    test_stats = model.test(test_set)

    assert test_stats['roc']['auc'] > 0.5


def pickle_and_unpickle(model):
    f = BytesIO()
    model.dump(f)
    f.seek(0)  # Rewind the file
    reconstructed_model = MLScorerModel.load(f)
    eq_([feature.name for feature in reconstructed_model.features],
        [feature.name for feature in model.features])
    eq_(type(reconstructed_model), type(model))
    train_score(reconstructed_model)


def get_and_format_info(model):

    assert model.info() is not None
    print(model.format_info())
