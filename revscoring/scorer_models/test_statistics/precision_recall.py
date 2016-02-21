import io

from sklearn.metrics import average_precision_score, precision_recall_curve
from tabulate import tabulate

from .test_statistic import ClassifierStatistic, TestStatistic


class precision_recall(ClassifierStatistic):
    """
    Constructs a precision/recall statistics generator.
    See https://en.wikipedia.org/wiki/Precision_and_recall

    When applied to a test set, the `score()` method will return a dictionary
    with four fields:

     * auc: the area under the precision-recall curve
     * precisions: a list of precisions
     * recalls: a list of recalls
     * thresholds: a list of probability thresholds
    """

    @classmethod
    def _single_class_stat(cls, scores, labels, comparison_label):
        y_proba = [s['probability'][comparison_label] for s in scores]

        y_true = [l == comparison_label for l in labels]
        precisions, recalls, thresholds = \
            precision_recall_curve(y_true, y_proba)

        return {
            'auc': average_precision_score(y_true, y_proba),
            'precisions': precisions,
            'recalls': recalls,
            'thresholds': thresholds
        }

    @classmethod
    def format(cls, stats, format="str"):
        if format == "str":
            return cls.format_str(stats)
        elif format == "json":
            if 'auc' in stats:
                return {
                    'auc': round(stats['auc'], 3)
                }
            else:
                return {k: round(ss['auc'], 3) for k, ss in stats.items()}
        else:
            raise TypeError("Format '{0}' not available for {1}."
                            .format(format, cls.__name__))

    @classmethod
    def format_str(cls, stats):
        formatted = io.StringIO()

        if 'auc' in stats and 'thresholds' in stats:
            # Single class
            formatted.write("PR-AUC: {0}".format(round(stats['auc'], 3)))
        else:
            # multiple classes
            formatted.write("PR-AUC:\n")

            table_data = [(repr(label), round(stats[label]['auc'], 3))
                          for label in sorted(stats.keys())]
            formatted.write("".join(["\t" + line + "\n" for line in
                                     tabulate(table_data).split("\n")]))

        return formatted.getvalue()

TestStatistic.register("precision_recall", precision_recall)
TestStatistic.register("pr", precision_recall)  # Backwards compatible
