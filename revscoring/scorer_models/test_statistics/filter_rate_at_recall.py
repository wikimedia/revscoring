import io

from sklearn.metrics import recall_score
from tabulate import tabulate

from . import util
from .test_statistic import ClassifierStatistic, TestStatistic


class filter_rate_at_recall(ClassifierStatistic):
    """
    Constructs a statistics generator that measures the maximum filter rate
    that can be achieved at minum recalle.  As a classifier gets better, the
    attainable filter rate at high recall values should go up.

    When applied to a test set, the `score()` method will return a dictionary
    with three fields:

     * threshold: The probability threshold where filter rate was maximized
     * filter_rate: The filter rate at `threshold`
     * recall: The recall at `threshold`

    :Parameters:
        min_recall : `float`
            The minimum recall proportion that will be tolerated
    """
    def __init__(self, min_recall):
        self.min_recall = min_recall
        super().__init__(min_recall=min_recall)

    def _single_class_stat(self, scores, labels, comparison_label):
        y_proba = [s['probability'][comparison_label] for s in scores]
        y_true = [label == comparison_label for label in labels]

        probas = set(y_proba)
        proba_rate_recalls = [
            (proba, util.filter_rate_score([p >= proba for p in y_proba]),
             recall_score(y_true, [p >= proba for p in y_proba]))
            for proba in probas
        ]
        filtered = [(proba, filter_rate, recall)
                    for proba, filter_rate, recall in proba_rate_recalls
                    if recall >= self.min_recall]

        if len(filtered) == 0:
            return {
                'threshold': None,
                'filter_rate': None,
                'recall': None
            }
        else:
            filtered.sort(key=lambda v: v[1], reverse=True)
            return dict(zip(['threshold', 'filter_rate', 'recall'],
                            filtered[0]))

    def format(self, stats, format="str"):
        if format == "str":
            return self.format_str(stats)
        elif format == "json":
            return util.round_floats(stats, 3)
        else:
            raise TypeError("Format '{0}' not available for {1}."
                            .format(format, self.__class__.__name__))

    def format_str(self, stats):
        formatted = io.StringIO()

        if 'threshold' in stats and 'filter_rate' in stats:
            # Single class
            formatted.write("Filter rate @ {0} recall: "
                            .format(self.min_recall))
            formatted.write(
                "threshold={0}, filter_rate={1}, recall={2}"
                .format(util.round_or_none(stats['threshold'], 3),
                        util.round_or_none(stats['filter_rate'], 3),
                        util.round_or_none(stats['recall'], 3)))
        else:
            # multiple classes
            formatted.write("Filter rate @ {0} recall:\n"
                            .format(self.min_recall))

            table_data = [(repr(label),
                           util.round_or_none(stats[label]['threshold'], 3),
                           util.round_or_none(stats[label]['filter_rate'], 3),
                           util.round_or_none(stats[label]['recall'], 3))
                          for label in sorted(stats.keys())]
            table = tabulate(table_data, headers=["label", "threshold",
                                                  "filter_rate", "recall"])
            formatted.write("".join(["\t" + line + "\n" for line in
                                     table.split("\n")]))

        return formatted.getvalue()

TestStatistic.register("filter_rate_at_recall", filter_rate_at_recall)
