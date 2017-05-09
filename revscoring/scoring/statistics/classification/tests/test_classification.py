import json

from nose.tools import eq_

from ..classification import Classification

LABELS = [True, False]
pool = \
    [({'prediction': i / 100 >= 0.5,
       'probability': {True: i / 100, False: 1 - (i / 100)}},
      (False if (i < 50 and i % 10 != 3) or i % 10 == 5 else True))
     for i in range(0, 101)] + \
    [({'prediction': i / 100 >= 0.5,
       'probability': {True: i / 100, False: 1 - (i / 100)}}, False)
     for i in range(0, 51)] * 39

SKEWED_PROBA = \
    [(s, l) for (s, l) in pool if l][:51] + \
    [(s, l) for (s, l) in pool if not l][:1949]

BALANCED_PROBA = \
    ([(s, l) for (s, l) in pool if l] * 20)[:1000] + \
    [(s, l) for (s, l) in pool if not l][:1000]


def test_classification():
    stats = Classification(
        prediction_key="prediction",
        decision_key="probability",
        labels=LABELS, population_rates={True: 0.05, False: 0.95})
    stats.fit(SKEWED_PROBA)

    stats.format_str({})
    json.dumps(stats.format_json({}), indent=2)

    counts_doc = stats.format_json({"counts": {}})['counts']
    eq_(counts_doc['n'], 2000)
    eq_(counts_doc['labels'][True], 51)
    eq_(counts_doc['predictions'][True][True], 46)

    rates_doc = stats.format_json({"rates": {}})['rates']
    eq_(rates_doc['sample'][True], 0.026)
    eq_(rates_doc['population'][True], 0.05)

    rates_doc = stats.format_json({"roc_auc": {}})['roc_auc']
    eq_(rates_doc['micro'], 0.952)
    eq_(rates_doc['macro'], 0.05)
