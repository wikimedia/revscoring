from ..threshold_classification import (ThresholdClassification,
                                        ThresholdOptimization)




def test_thresholds():
    recall_at_precision_90 = ThresholdOptimization.parse(
        "maximum recall @ precision >= 0.9")
    match_rate_at_recall_90 = ThresholdOptimization.parse(
        "minimum match_rate @ recall >= 0.9")
    natural_thresholds = ThresholdClassification(
        labels=LABELS, population_rates={True: 0.05, False: 0.95},
        max_thresholds=10,
        threshold_optimizations=[recall_at_precision_90,
                                 match_rate_at_recall_90])
    natural_thresholds.fit(score_labels)
    print(natural_thresholds.format(
        ['accuracy', 'pr_auc', 'roc_auc',
         'maximum recall @ precision >= 0.9',
         'minimum match_rate @ recall >= 0.9',
         'thresholds'],
        formatting="str"))

    scaled_thresholds = ThresholdClassification(
        labels=LABELS, population_rates={True: 0.05, False: 0.95},
        max_thresholds=10,
        threshold_optimizations=[recall_at_precision_90,
                                 match_rate_at_recall_90])
    scaled_thresholds.fit(balanced_score_labels)
    print(scaled_thresholds.format(
        ['accuracy', 'pr_auc', 'roc_auc',
         'maximum recall @ precision >= 0.9',
         'minimum match_rate @ recall >= 0.9',
         'thresholds'],
        formatting="str"))

    count = 0
    squared_error = 0
    error = 0
    for label in natural_thresholds['thresholds']:
        nl_thresholds = natural_thresholds['thresholds'][label].format_json()
        sl_thresholds = scaled_thresholds['thresholds'][label].format_json()
        for n_stats, s_stats in zip(nl_thresholds, sl_thresholds):

            for stat_name in n_stats:
                if n_stats[stat_name] is not None:
                    count += 1
                    diff = n_stats[stat_name] - s_stats[stat_name]
                    squared_error += diff**2
                    error += diff

    rmse = (squared_error / count)**0.5
    print("RMSE", rmse)
    assert rmse < 0.05
