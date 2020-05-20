
from revscoring.scoring.statistics.classification.scaled_prediction_statistics import \
    ScaledPredictionStatistics # noqa

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


def test_ls_balanced():
    y_pred, y_trues = zip(*((s['prediction'], l) for s, l in BALANCED))
    sps = ScaledPredictionStatistics(y_pred, y_trues)
    print(sps.format_str({}))
    assert ((sps.tp, sps.fp, sps.tn, sps.fn) ==
            (50, 50, 50, 50))
    assert sps['match_rate'] == 100 / 200
    assert sps['filter_rate'] == 100 / 200
    assert sps['precision'] == 50 / 100
    assert sps['!precision'] == 50 / 100
    assert sps['recall'] == 50 / 100
    assert sps['!recall'] == 50 / 100
    assert sps['accuracy'] == 100 / 200
    assert sps['fpr'] == 50 / 100
    assert (sps['f1'] ==
            2 * (((1 / 2) * (1 / 2)) /
                 ((1 / 2) + (1 / 2))))
    assert (sps['!f1'] ==
            2 * (((1 / 2) * (1 / 2)) /
                 ((1 / 2) + (1 / 2))))
    assert (sps.format_json({'precision': {}, 'recall': {}}) ==
            {'precision': 50 / 100, 'recall': 50 / 100})


def test_ls_balanced_scaled():
    # Balanced, scaled
    y_pred, y_trues = zip(*((s['prediction'], l) for s, l in BALANCED))
    sps = ScaledPredictionStatistics(y_pred, y_trues, population_rate=0.05)
    print(sps.format_str({}))
    assert ((sps.tp, sps.fp, sps.tn, sps.fn) ==
            (5, 95, 95, 5))
    assert sps['match_rate'] == 100 / 200
    assert sps['filter_rate'] == 100 / 200
    assert sps['precision'] == 5 / 100
    assert sps['!precision'] == 95 / 100
    assert sps['recall'] == 5 / 10
    assert sps['!recall'] == 95 / 190
    assert sps['accuracy'] == 100 / 200
    assert sps['fpr'] == 5 / 10
    assert (sps['f1'] ==
            2 * (((5 / 10) * (5 / 100)) /
                 ((5 / 10) + (5 / 100))))
    assert (sps['!f1'] ==
            2 * (((95 / 190) * (95 / 100)) /
                 ((95 / 190) + (95 / 100))))
    assert (sps.format_json({'precision': {}, 'recall': {}}) ==
            {'precision': 5 / 100, 'recall': 5 / 10})


def test_ls_good():
    y_pred, y_trues = zip(*((s['prediction'], l) for s, l in GOOD))
    sps = ScaledPredictionStatistics(y_pred, y_trues, population_rate=0.05)
    assert ((sps.tp, sps.fp, sps.tn, sps.fn) ==
            (9.5, 9.5, 180.5, 0.5))

    print(sps.format_str({}))
    assert sps['match_rate'] == 19 / 200
    assert sps['filter_rate'] == 181 / 200
    assert sps['precision'] == 9.5 / 19
    assert sps['!precision'] == 180.5 / 181
    assert sps['recall'] == 95 / 100
    assert sps['!recall'] == 95 / 100
    assert sps['accuracy'] == 190 / 200
    assert sps['fpr'] == 9.5 / 190
    assert sps.n == 200
    assert sps.tp == 9.5
    assert (sps['f1'] ==
            2 * (((9.5 / 19) * (95 / 100)) /
                 ((9.5 / 19) + (95 / 100))))
    assert (sps['!f1'] ==
            2 * (((180.5 / 181) * (95 / 100)) /
                 ((180.5 / 181) + (95 / 100))))
    assert (sps.format_json({'precision': {}, 'recall': {}}) ==
            {'precision': 9.5 / 19, 'recall': 95 / 100})


def test_ls_perfect():
    y_pred, y_trues = zip(*((s['prediction'], l) for s, l in PERFECT))
    sps = ScaledPredictionStatistics(y_pred, y_trues, population_rate=0.05)
    print(sps.format_str({}))
    assert ((sps.tp, sps.fp, sps.tn, sps.fn) ==
            (10, 0, 190, 0))
    assert sps['match_rate'] == 10 / 200
    assert sps['filter_rate'] == 190 / 200
    assert sps['precision'] == 1
    assert sps['!precision'] == 1
    assert sps['recall'] == 1
    assert sps['!recall'] == 1
    assert sps['accuracy'] == 1
    assert sps['fpr'] == 0
    assert sps['f1'] == 1
    assert sps['!f1'] == 1
    assert (sps.format_json({'precision': {}, 'recall': {}}) ==
            {'precision': 1, 'recall': 1})


def test_ls_the_worst():
    y_pred, y_trues = zip(*((s['prediction'], l) for s, l in WORST))
    sps = ScaledPredictionStatistics(y_pred, y_trues, population_rate=0.05)
    print(sps.format_str({}))
    assert ((sps.tp, sps.fp, sps.tn, sps.fn) ==
            (0, 190, 0, 10))
    assert sps['match_rate'] == 190 / 200
    assert sps['filter_rate'] == 1 - (190 / 200)
    assert sps['precision'] == 0
    assert sps['!precision'] == 0
    assert sps['recall'] == 0
    assert sps['!recall'] == 0
    assert sps['accuracy'] == 0
    assert sps['fpr'] == 1
    assert sps['f1'] is None
    assert sps['!f1'] is None
    assert (sps.format_json({'precision': {}, 'recall': {}}) ==
            {'precision': 0, 'recall': 0})
