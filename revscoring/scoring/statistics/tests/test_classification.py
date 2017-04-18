import json

from nose.tools import eq_

from ..classification import Classification, LabelStatistics

LABELS = [True, False]
BALANCED = ([({'prediction': True}, True) for i in range(50)] +   # TP
            [({'prediction': False}, True) for i in range(50)] +  # FN
            [({'prediction': True}, False) for i in range(50)] +  # FP
            [({'prediction': False}, False) for i in range(50)])  # TN
PERFECT = ([({'prediction': True}, True) for i in range(100)] +   # TP
           [({'prediction': False}, True) for i in range(0)] +  # FN
           [({'prediction': True}, False) for i in range(0)] +  # FP
           [({'prediction': False}, False) for i in range(100)])  # TN
WORST = ([({'prediction': True}, True) for i in range(0)] +   # TP
         [({'prediction': False}, True) for i in range(100)] +  # FN
         [({'prediction': True}, False) for i in range(100)] +  # FP
         [({'prediction': False}, False) for i in range(0)])  # TN
GOOD = ([({'prediction': True}, True) for i in range(95)] +   # TP
        [({'prediction': False}, True) for i in range(5)] +  # FN
        [({'prediction': True}, False) for i in range(5)] +  # FP
        [({'prediction': False}, False) for i in range(95)])  # TN


def test_classification():

    stats = Classification(
        labels=LABELS, population_rates={True: 0.05, False: 0.95})
    stats.fit(GOOD)

    print(stats.format(formatting="str"))
    print(json.dumps(stats.format(formatting="json"), indent=2))


def test_ls_balanced():
    y_pred, y_trues = zip(*((s['prediction'], l) for s, l in BALANCED))
    ls = LabelStatistics(y_pred, y_trues)
    print(ls.format(formatting="str"))
    eq_((ls.tp, ls.fp, ls.tn, ls.fn),
        (50, 50, 50, 50))
    eq_(ls.get_stat('match_rate'), 100 / 200)
    eq_(ls.get_stat('filter_rate'), 100 / 200)
    eq_(ls.get_stat('precision'), 50 / 100)
    eq_(ls.get_stat('!precision'), 50 / 100)
    eq_(ls.get_stat('recall'), 50 / 100)
    eq_(ls.get_stat('!recall'), 50 / 100)
    eq_(ls.get_stat('accuracy'), 100 / 200)
    eq_(ls.get_stat('fpr'), 50 / 100)
    eq_(ls.get_stat('f1'),
        2 * (((1 / 2) * (1 / 2)) /
             ((1 / 2) + (1 / 2))))
    eq_(ls.get_stat('!f1'),
        2 * (((1 / 2) * (1 / 2)) /
             ((1 / 2) + (1 / 2))))
    eq_(ls.format_json(['precision', 'recall']),
        {'precision': 50 / 100, 'recall': 50 / 100})


def test_ls_balanced_scaled():
    # Balanced, scaled
    y_pred, y_trues = zip(*((s['prediction'], l) for s, l in BALANCED))
    ls = LabelStatistics(y_pred, y_trues, population_rate=0.05)
    print(ls.format(formatting="str"))
    eq_((ls.tp, ls.fp, ls.tn, ls.fn),
        (5, 95, 95, 5))
    eq_(ls.get_stat('match_rate'), 100 / 200)
    eq_(ls.get_stat('filter_rate'), 100 / 200)
    eq_(ls.get_stat('precision'), 5 / 100)
    eq_(ls.get_stat('!precision'), 95 / 100)
    eq_(ls.get_stat('recall'), 5 / 10)
    eq_(ls.get_stat('!recall'), 95 / 190)
    eq_(ls.get_stat('accuracy'), 100 / 200)
    eq_(ls.get_stat('fpr'), 5 / 10)
    eq_(ls.get_stat('f1'),
        2 * (((5 / 10) * (5 / 100)) /
             ((5 / 10) + (5 / 100))))
    eq_(ls.get_stat('!f1'),
        2 * (((95 / 190) * (95 / 100)) /
             ((95 / 190) + (95 / 100))))
    eq_(ls.format_json(['precision', 'recall']),
        {'precision': 5 / 100, 'recall': 5 / 10})


def test_ls_good():
    y_pred, y_trues = zip(*((s['prediction'], l) for s, l in GOOD))
    ls = LabelStatistics(y_pred, y_trues, population_rate=0.05)
    eq_((ls.tp, ls.fp, ls.tn, ls.fn),
        (9.5, 9.5, 180.5, 0.5))

    print(ls.format(formatting="str"))
    eq_(ls.get_stat('match_rate'), 19 / 200)
    eq_(ls.get_stat('filter_rate'), 181 / 200)
    eq_(ls.get_stat('precision'), 9.5 / 19)
    eq_(ls.get_stat('!precision'), 180.5 / 181)
    eq_(ls.get_stat('recall'), 95 / 100)
    eq_(ls.get_stat('!recall'), 95 / 100)
    eq_(ls.get_stat('accuracy'), 190 / 200)
    eq_(ls.get_stat('fpr'), 9.5 / 190)
    eq_(ls.n, 200)
    eq_(ls.tp, 9.5)
    eq_(ls.get_stat('f1'),
        2 * (((9.5 / 19) * (95 / 100)) /
             ((9.5 / 19) + (95 / 100))))
    eq_(ls.get_stat('!f1'),
        2 * (((180.5 / 181) * (95 / 100)) /
             ((180.5 / 181) + (95 / 100))))
    eq_(ls.format_json(['precision', 'recall']),
        {'precision': 9.5 / 19, 'recall': 95 / 100})


def test_ls_perfect():
    y_pred, y_trues = zip(*((s['prediction'], l) for s, l in PERFECT))
    ls = LabelStatistics(y_pred, y_trues, population_rate=0.05)
    print(ls.format(formatting="str"))
    eq_((ls.tp, ls.fp, ls.tn, ls.fn),
        (10, 0, 190, 0))
    eq_(ls.get_stat('match_rate'), 10 / 200)
    eq_(ls.get_stat('filter_rate'), 190 / 200)
    eq_(ls.get_stat('precision'), 1)
    eq_(ls.get_stat('!precision'), 1)
    eq_(ls.get_stat('recall'), 1)
    eq_(ls.get_stat('!recall'), 1)
    eq_(ls.get_stat('accuracy'), 1)
    eq_(ls.get_stat('fpr'), 0)
    eq_(ls.get_stat('f1'), 1)
    eq_(ls.get_stat('!f1'), 1)
    eq_(ls.format_json(['precision', 'recall']),
        {'precision': 1, 'recall': 1})


def test_ls_the_worst():
    y_pred, y_trues = zip(*((s['prediction'], l) for s, l in WORST))
    ls = LabelStatistics(y_pred, y_trues, population_rate=0.05)
    print(ls.format(formatting="str"))
    eq_((ls.tp, ls.fp, ls.tn, ls.fn),
        (0, 190, 0, 10))
    eq_(ls.get_stat('match_rate'), 190 / 200)
    eq_(ls.get_stat('filter_rate'), 1 - (190 / 200))
    eq_(ls.get_stat('precision'), 0)
    eq_(ls.get_stat('!precision'), 0)
    eq_(ls.get_stat('recall'), 0)
    eq_(ls.get_stat('!recall'), 0)
    eq_(ls.get_stat('accuracy'), 0)
    eq_(ls.get_stat('fpr'), 1)
    eq_(ls.get_stat('f1'), None)
    eq_(ls.get_stat('!f1'), None)
    eq_(ls.format_json(['precision', 'recall']),
        {'precision': 0, 'recall': 0})
