import io
import logging
from collections import defaultdict

from numpy import linspace
from scipy import interp
from sklearn.metrics import (auc, average_precision_score,
                             precision_recall_curve)
from tabulate import tabulate

from .test_statistic import ClassifierStatistic, TestStatistic

logger = logging.getLogger(__name__)


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
            'precisions': list(precisions),
            'recalls': list(recalls)
        }

    def merge(self, stats):
        individual_auc = defaultdict(list)
        label_sum_recalls = defaultdict(float)
        for stat in stats:
            for label, label_stat in stat.items():
                individual_auc[label].append(label_stat['auc'])
                precisions, recalls = \
                    label_stat['precisions'], label_stat['recalls']
                label_sum_recalls[label] += \
                    interp(linspace(0, 1, 100), precisions, recalls)

        merged_stat = {}
        for label, sum_recalls in label_sum_recalls.items():
            mean_recalls = sum_recalls / len(stats)
            interp_auc = auc(linspace(0, 1, 100), mean_recalls)
            logger.debug("interp_auc={0}, individual_auc={1}"
                          .format(interp_auc, individual_auc[label]))

            merged_stat[label] = {
                'auc': interp_auc,
                'precisions': list(linspace(0, 1, 100)),
                'recalls': list(mean_recalls)
            }

        return merged_stat

    @classmethod
    def format(cls, stat, format="str"):
        if format == "str":
            return cls.format_str(stat)
        elif format == "json":
            return {label: {'auc': round(ss['auc'], 3)}
                    for label, ss in stat.items()}
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
