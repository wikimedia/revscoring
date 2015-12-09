from sklearn.metrics import auc, make_scorer, precision_recall_curve

SCORERS = {}


def pr_auc_score(y_true, y_score):
    """
    Generates the Area Under the Curve for precision and recall.
    """
    precision, recall, thresholds = \
        precision_recall_curve(y_true, y_score[:, 1])
    return auc(recall, precision, reorder=True)

pr_auc_scorer = make_scorer(pr_auc_score, greater_is_better=True,
                            needs_proba=True)

SCORERS['pr_auc'] = pr_auc_scorer
