import json

from revscoring.scoring.statistics.classification.counts import Counts
from revscoring.scoring.statistics.classification.rates import Rates

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


def test_wide_labels():
    long_counts = Counts(
        ["I have a bunch of characters",
         "And I'm going to take up way too much space",
         "This is definitely going to be too long"],
        [({'prediction': "I have a bunch of characters"},
          "I have a bunch of characters")] * 30 +
        [({'prediction': "I have a bunch of characters"},
          "And I'm going to take up way too much space")] * 2 +
        [({'prediction': "I have a bunch of characters"},
          "This is definitely going to be too long")] * 1 +
        [({'prediction': "And I'm going to take up way too much space"},
          "And I'm going to take up way too much space")] * 25 +
        [({'prediction': "And I'm going to take up way too much space"},
          "I have a bunch of characters")] * 5 +
        [({'prediction': "And I'm going to take up way too much space"},
          "This is definitely going to be too long")] * 6 +
        [({'prediction': "This is definitely going to be too long"},
          "This is definitely going to be too long")] * 35 +
        [({'prediction': "This is definitely going to be too long"},
          "I have a bunch of characters")] * 1 +
        [({'prediction': "This is definitely going to be too long"},
          "And I'm going to take up way too much space")] * 1,
        'prediction')
    r = Rates(long_counts, population_rates={
        "I have a bunch of characters": 0.45,
         "And I'm going to take up way too much space": 0.332,
         "This is definitely going to be too long": 0.25
    })
    print(r.format_str({}))
    lines = r.format_str({}).split("\n")
    for line in lines:
        assert len(line) < 80
