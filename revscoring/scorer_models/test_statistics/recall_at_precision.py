import io
from collections import defaultdict

from sklearn.metrics import precision_score, recall_score
from tabulate import tabulate

from . import util
from .test_statistic import ClassifierStatistic, TestStatistic


class recall_at_precision(ClassifierStatistic):
    """
    Constructs a statistics generator that measures the maximum recall
    that can be achieved at minimum precision.  As a classifier
    gets better, the attainable recall at precision should increase.

    When applied to a test set, the `score()` method will return a dictionary
    with three fields:

     * threshold: The probability threshold where recall was maximized
     * recall: The recall at `threshold`
     * precision: The precision at `threshold`

    :Parameters:
        min_precision : `float`
            Minimum precision that will be tolerated
    """
    def __init__(self, min_precision):
        self.min_precision = min_precision
        super().__init__(min_precision=min_precision)

    def _single_class_stat(self, scores, labels, comparison_label):
        y_proba = [s['probability'][comparison_label] for s in scores]
        y_true = [label == comparison_label for label in labels]

        probas = set(y_proba)
        proba_recall_precision = [
            (proba, recall_score(y_true, [p >= proba for p in y_proba]),
             precision_score(y_true, [p >= proba for p in y_proba]))
            for proba in probas
        ]
        filtered = [(proba, recall, precision)
                    for proba, recall, precision in proba_recall_precision
                    if precision >= self.min_precision]

        if len(filtered) == 0:
            return {
                'threshold': None,
                'recall': None,
                'precision': None
            }
        else:
            filtered.sort(key=lambda v: v[1], reverse=True)
            return dict(zip(['threshold', 'recall', 'precision'], filtered[0]))

    def merge(self, stats):
        label_vals = defaultdict(lambda: defaultdict(list))

        for stat in stats:
            for label, label_stat in stat.items():
                label_vals[label]['threshold'].append(label_stat['threshold'])
                label_vals[label]['recall'].append(label_stat['recall'])
                label_vals[label]['precision'].append(label_stat['precision'])

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
        formatted.write("Recall @ {0} precision:\n"
                        .format(self.min_precision))

        table_data = [(repr(label),
                       util.round_or_none(stat[label]['threshold'], 3),
                       util.round_or_none(stat[label]['recall'], 3),
                       util.round_or_none(stat[label]['precision'], 3))
                      for label in sorted(stat.keys())]
        table = tabulate(
            table_data, headers=["label", "threshold", "recall", "precision"])
        formatted.write("".join(["\t" + line + "\n" for line in
                                 table.split("\n")]))

        return formatted.getvalue()

TestStatistic.register("recall_at_precision", recall_at_precision)
