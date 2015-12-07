from sklearn.metrics import auc, precision_recall_curve


def pr_auc_score(y_true, y_score):
    precision, recall, thresholds = precision_recall_curve(y_true, y_score)
    return auc(recall, precision)
