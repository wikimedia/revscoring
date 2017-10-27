import json


from ..counts import Counts
from ..rates import Rates

COUNTS = Counts(
    [True, False],
    [({'prediction': True}, True)] * 10 +
    [({'prediction': True}, False)] * 20 +
    [({'prediction': False}, False)] * 30 +
    [({'prediction': False}, True)] * 40,
    'prediction')


def test_simple():
    r = Rates(COUNTS)

    print(r.format_str({}))
    print(json.dumps(r.format_json({}), indent=2))
    assert r.lookup("sample.true") == 0.5
    assert r.lookup("sample.false") == 0.5


def test_population():
    r = Rates(COUNTS, population_rates={True: 0.05, False: 0.95})
    print(r.format_str({}))
    print(json.dumps(r.format_json({}), indent=2))
    assert r.lookup("sample.true") == 0.5
    assert r.lookup("sample.false") == 0.5
    assert r.lookup("population.true") == 0.05
    assert r.lookup("population.false") == 0.95
