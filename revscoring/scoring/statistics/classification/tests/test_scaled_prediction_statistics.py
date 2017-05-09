from nose.tools import eq_

from ..scaled_prediction_statistics import ScaledPredictionStatistics

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
    eq_((sps.tp, sps.fp, sps.tn, sps.fn),
        (50, 50, 50, 50))
    eq_(sps['match_rate'], 100 / 200)
    eq_(sps['filter_rate'], 100 / 200)
    eq_(sps['precision'], 50 / 100)
    eq_(sps['!precision'], 50 / 100)
    eq_(sps['recall'], 50 / 100)
    eq_(sps['!recall'], 50 / 100)
    eq_(sps['accuracy'], 100 / 200)
    eq_(sps['fpr'], 50 / 100)
    eq_(sps['f1'],
        2 * (((1 / 2) * (1 / 2)) /
             ((1 / 2) + (1 / 2))))
    eq_(sps['!f1'],
        2 * (((1 / 2) * (1 / 2)) /
             ((1 / 2) + (1 / 2))))
    eq_(sps.format_json({'precision': {}, 'recall': {}}),
        {'precision': 50 / 100, 'recall': 50 / 100})


def test_ls_balanced_scaled():
    # Balanced, scaled
    y_pred, y_trues = zip(*((s['prediction'], l) for s, l in BALANCED))
    sps = ScaledPredictionStatistics(y_pred, y_trues, population_rate=0.05)
    print(sps.format_str({}))
    eq_((sps.tp, sps.fp, sps.tn, sps.fn),
        (5, 95, 95, 5))
    eq_(sps['match_rate'], 100 / 200)
    eq_(sps['filter_rate'], 100 / 200)
    eq_(sps['precision'], 5 / 100)
    eq_(sps['!precision'], 95 / 100)
    eq_(sps['recall'], 5 / 10)
    eq_(sps['!recall'], 95 / 190)
    eq_(sps['accuracy'], 100 / 200)
    eq_(sps['fpr'], 5 / 10)
    eq_(sps['f1'],
        2 * (((5 / 10) * (5 / 100)) /
             ((5 / 10) + (5 / 100))))
    eq_(sps['!f1'],
        2 * (((95 / 190) * (95 / 100)) /
             ((95 / 190) + (95 / 100))))
    eq_(sps.format_json({'precision': {}, 'recall': {}}),
        {'precision': 5 / 100, 'recall': 5 / 10})


def test_ls_good():
    y_pred, y_trues = zip(*((s['prediction'], l) for s, l in GOOD))
    sps = ScaledPredictionStatistics(y_pred, y_trues, population_rate=0.05)
    eq_((sps.tp, sps.fp, sps.tn, sps.fn),
        (9.5, 9.5, 180.5, 0.5))

    print(sps.format_str({}))
    eq_(sps['match_rate'], 19 / 200)
    eq_(sps['filter_rate'], 181 / 200)
    eq_(sps['precision'], 9.5 / 19)
    eq_(sps['!precision'], 180.5 / 181)
    eq_(sps['recall'], 95 / 100)
    eq_(sps['!recall'], 95 / 100)
    eq_(sps['accuracy'], 190 / 200)
    eq_(sps['fpr'], 9.5 / 190)
    eq_(sps.n, 200)
    eq_(sps.tp, 9.5)
    eq_(sps['f1'],
        2 * (((9.5 / 19) * (95 / 100)) /
             ((9.5 / 19) + (95 / 100))))
    eq_(sps['!f1'],
        2 * (((180.5 / 181) * (95 / 100)) /
             ((180.5 / 181) + (95 / 100))))
    eq_(sps.format_json({'precision': {}, 'recall': {}}),
        {'precision': 9.5 / 19, 'recall': 95 / 100})


def test_ls_perfect():
    y_pred, y_trues = zip(*((s['prediction'], l) for s, l in PERFECT))
    sps = ScaledPredictionStatistics(y_pred, y_trues, population_rate=0.05)
    print(sps.format_str({}))
    eq_((sps.tp, sps.fp, sps.tn, sps.fn),
        (10, 0, 190, 0))
    eq_(sps['match_rate'], 10 / 200)
    eq_(sps['filter_rate'], 190 / 200)
    eq_(sps['precision'], 1)
    eq_(sps['!precision'], 1)
    eq_(sps['recall'], 1)
    eq_(sps['!recall'], 1)
    eq_(sps['accuracy'], 1)
    eq_(sps['fpr'], 0)
    eq_(sps['f1'], 1)
    eq_(sps['!f1'], 1)
    eq_(sps.format_json({'precision': {}, 'recall': {}}),
        {'precision': 1, 'recall': 1})


def test_ls_the_worst():
    y_pred, y_trues = zip(*((s['prediction'], l) for s, l in WORST))
    sps = ScaledPredictionStatistics(y_pred, y_trues, population_rate=0.05)
    print(sps.format_str({}))
    eq_((sps.tp, sps.fp, sps.tn, sps.fn),
        (0, 190, 0, 10))
    eq_(sps['match_rate'], 190 / 200)
    eq_(sps['filter_rate'], 1 - (190 / 200))
    eq_(sps['precision'], 0)
    eq_(sps['!precision'], 0)
    eq_(sps['recall'], 0)
    eq_(sps['!recall'], 0)
    eq_(sps['accuracy'], 0)
    eq_(sps['fpr'], 1)
    eq_(sps['f1'], None)
    eq_(sps['!f1'], None)
    eq_(sps.format_json({'precision': {}, 'recall': {}}),
        {'precision': 0, 'recall': 0})
