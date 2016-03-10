import numpy
from nose.tools import eq_

from ..util import balance_sample, balance_sample_weights, normalize_json


def test_normalize_json():
    doc = {"foo": {numpy.bool_(True): "value"}, "what": numpy.bool_(False)}
    normalized_doc = normalize_json(doc)
    eq_(type(normalized_doc['what']), bool)
    eq_(type(list(normalized_doc['foo'].keys())[0]), bool)


def test_balance_sample():
    sample = [((1, 2, 3), True),
              ((1, 2, 3), True),
              ((1, 2, 3), True),
              ((1, 2, 3), True),
              ((1, 2, 3), True),
              ((1, 2, 3), False),
              ((1, 2, 3), False)]

    balanced_sample = balance_sample(sample)

    counts = {}
    for _, label in balanced_sample:
        counts[label] = counts.get(label, 0) + 1

    eq_(counts[True], 5)
    eq_(counts[False], 5)


def test_balance_sample_weights():
    sample = [((1, 2, 3), True),
              ((1, 2, 3), True),
              ((1, 2, 3), True),
              ((1, 2, 3), True),
              ((1, 2, 3), True),
              ((1, 2, 3), False),
              ((1, 2, 3), False)]

    weights = balance_sample_weights(sample)

    eq_(weights,
        [7 / 5, 7 / 5, 7 / 5, 7 / 5, 7 / 5,
         7 / 2, 7 / 2])
