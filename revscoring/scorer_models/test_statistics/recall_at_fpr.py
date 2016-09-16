import io
from collections import defaultdict

from sklearn.metrics import recall_score
from tabulate import tabulate

from . import util
from .test_statistic import ClassifierStatistic, TestStatistic


class recall_at_fpr(ClassifierStatistic):
    """
    Constructs a statistics generator that measures the maximum recall
    that can be achieved at maximum false-positive rate.  As a classifier
    gets better, the attainable recall at low false-positive rates should
    increase.

    When applied to a test set, the `score()` method will return a dictionary
    with three fields:

     * threshold: The probability threshold where recall was maximized
     * recall: The recall at `threshold`
     * fpr: The false-positive rate at `threshold`

    :Parameters:
        max_fpr : `float`
            Maximum false-positive rate that will be tolerated
    """
    def __init__(self, max_fpr):
        self.max_fpr = max_fpr
        super().__init__(max_fpr=max_fpr)

    def _single_class_stat(self, scores, labels, comparison_label):
        y_proba = [s['probability'][comparison_label] for s in scores]
        y_true = [label == comparison_label for label in labels]

        probas = set(y_proba)
        proba_recall_fprs = [
            (proba, recall_score(y_true, [p >= proba for p in y_proba]),
             util.fpr_score(y_true, [p >= proba for p in y_proba]))
            for proba in probas
        ]
        filtered = [(proba, recall, fpr)
                    for proba, recall, fpr in proba_recall_fprs
                    if fpr <= self.max_fpr]

        if len(filtered) == 0:
            return {
                'threshold': None,
                'recall': None,
                'fpr': None
            }
        else:
            filtered.sort(key=lambda v: v[1], reverse=True)
            return dict(zip(['threshold', 'recall', 'fpr'], filtered[0]))

    def merge(self, stats):
        label_vals = defaultdict(lambda: defaultdict(list))

        for stat in stats:
            for label, label_stat in stat.items():
                label_vals[label]['threshold'].append(label_stat['threshold'])
                label_vals[label]['recall'].append(label_stat['recall'])
                label_vals[label]['fpr'].append(label_stat['fpr'])

        merged_stats = {}
        for label, metric_vals in label_vals.items():
            merged_stats[label] = \
                {name: util.mean_or_none(vals)
                 for name, vals in metric_vals.items()}

        return merged_stats

    def format(self, stats, format="str"):
        if format == "str":
            return self.format_str(stats)
        elif format == "json":
            return util.round_floats(stats, 3)
        else:
            raise TypeError("Format '{0}' not available for {1}."
                            .format(format, self.__name__))

    def format_str(self, stat):
        formatted = io.StringIO()
        formatted.write("Recall @ {0} false-positive rate:\n"
                        .format(self.max_fpr))

        table_data = [(repr(label),
                       util.round_or_none(stat[label]['threshold'], 3),
                       util.round_or_none(stat[label]['recall'], 3),
                       util.round_or_none(stat[label]['fpr'], 3))
                      for label in sorted(stat.keys())]
        table = tabulate(
            table_data, headers=["label", "threshold", "recall", "fpr"])
        formatted.write("".join(["\t" + line + "\n" for line in
                                 table.split("\n")]))

        return formatted.getvalue()

TestStatistic.register("recall_at_fpr", recall_at_fpr)
