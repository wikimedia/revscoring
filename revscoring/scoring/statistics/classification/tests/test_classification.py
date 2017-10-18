import json
import pickle


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
    balanced_stats = Classification(
        prediction_key="prediction",
        decision_key="probability",
        labels=LABELS, population_rates={True: 0.05, False: 0.95})
    balanced_stats.fit(BALANCED_PROBA)
    skewed_stats = Classification(
        prediction_key="prediction",
        decision_key="probability",
        labels=LABELS, population_rates={True: 0.05, False: 0.95})
    skewed_stats.fit(SKEWED_PROBA)

    skewed_stats.format_str({})
    doc = skewed_stats.format_json({})
    assert "thresholds" not in doc

    json.dumps(doc, indent=2)

    balanced_stats.format_str({})
    json.dumps(balanced_stats.format_json({}), indent=2)

    skewed_doc = skewed_stats.format_json({"counts": {}})['counts']
    assert skewed_doc['n'] == 2000
    assert skewed_doc['labels'][True] == 51
    assert skewed_doc['predictions'][True][True] == 46
    balanced_doc = balanced_stats.format_json({"counts": {}})['counts']
    assert balanced_doc['n'] == 2000
    assert balanced_doc['labels'][True] == 1000
    assert balanced_doc['predictions'][True][True] == 900

    skewed_doc = skewed_stats.format_json({"rates": {}})['rates']
    assert skewed_doc['sample'][True] == 0.026
    assert skewed_doc['population'][True] == 0.05
    balanced_doc = balanced_stats.format_json({"rates": {}})['rates']
    assert balanced_doc['sample'][True] == 0.5
    assert balanced_doc['population'][True] == 0.05

    skewed_doc = skewed_stats.format_json({"roc_auc": {}})['roc_auc']
    assert skewed_doc['micro'] == 0.952
    assert skewed_doc['macro'] == 0.946
    balanced_doc = balanced_stats.format_json({"roc_auc": {}})['roc_auc']
    assert abs(balanced_doc['micro'] - skewed_doc['micro']) < 0.025, \
        str(abs(balanced_doc['micro'] - skewed_doc['micro']))
    assert abs(balanced_doc['macro'] - skewed_doc['macro']) < 0.025, \
        str(abs(balanced_doc['macro'] - skewed_doc['macro']))

    skewed_doc = skewed_stats.format_json({"pr_auc": {}})['pr_auc']
    assert skewed_doc['micro'] == 0.988
    assert skewed_doc['macro'] == 0.933
    balanced_doc = balanced_stats.format_json({"pr_auc": {}})['pr_auc']
    assert abs(balanced_doc['micro'] - skewed_doc['micro']) < 0.025, \
        str(abs(balanced_doc['micro'] - skewed_doc['micro']))
    assert abs(balanced_doc['macro'] - skewed_doc['macro']) < 0.025, \
        str(abs(balanced_doc['macro'] - skewed_doc['macro']))

    skewed_doc = skewed_stats.format_json({"accuracy": {}})['accuracy']
    assert skewed_doc['micro'] == 0.975
    assert skewed_doc['macro'] == 0.975
    balanced_doc = balanced_stats.format_json({"accuracy": {}})['accuracy']
    assert abs(balanced_doc['micro'] - skewed_doc['micro']) < 0.025, \
        str(abs(balanced_doc['micro'] - skewed_doc['micro']))
    assert abs(balanced_doc['macro'] - skewed_doc['macro']) < 0.025, \
        str(abs(balanced_doc['macro'] - skewed_doc['macro']))

    assert abs(skewed_stats.lookup('accuracy.micro') - 0.975) < 0.025, \
        str(skewed_stats.lookup('accuracy.micro') - 0.975)

    assert abs(skewed_stats.lookup('roc_auc.micro') - 0.975) < 0.025, \
        str(skewed_stats.lookup('roc_auc.micro') - 0.975)

    optimized = skewed_stats.lookup(
        '"maximum recall @ precision >= 0.9".labels.true')
    assert abs(optimized - 0.51) < 0.025, \
        str(optimized - 0.51)

    print(skewed_stats.format_str({"thresholds": {True: {}}},
                                  threshold_ndigits=3))

    # Optimization
    print(skewed_stats.format_str(
        {"thresholds": {True: {"maximum recall @ precision >= 0.9"}}},
        threshold_ndigits=3))

    print(vars(skewed_stats))
    pickle.loads(pickle.dumps(skewed_stats))
