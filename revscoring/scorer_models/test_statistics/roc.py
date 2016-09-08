import io
import logging
from collections import defaultdict

from numpy import linspace
from scipy import interp
from sklearn.metrics import auc, roc_curve
from tabulate import tabulate

from .test_statistic import ClassifierStatistic, TestStatistic

logger = logging.getLogger(__name__)


class roc(ClassifierStatistic):
    """
    Constructs a reciever operating characteristic statistics generator.
    See https://en.wikipedia.org/wiki/Receiver_operating_characteristic

    When applied to a test set, the `score()` method will return a dictionary
    with four fields:

     * auc: the area under the ROC curve
     * fprs: a list of false-positive rates
     * tprs: a list of true-positive rates
     * thresholds: a list of probability thresholds
    """
    @classmethod
    def _single_class_stat(cls, scores, labels, comparison_label):
        y_proba = [s['probability'][comparison_label] for s in scores]

        y_true = [l == comparison_label for l in labels]
        fprs, tprs, thresholds = roc_curve(y_true, y_proba)

        return {
            'auc': auc(fprs, tprs),
            'fprs': fprs,
            'tprs': tprs
        }

    def merge(self, stats):
        individual_auc = defaultdict(list)
        label_sum_tpr = defaultdict(float)
        for stat in stats:
            for label, label_stat in stat.items():
                individual_auc[label].append(label_stat['auc'])
                fprs, tprs = label_stat['fprs'], label_stat['tprs']
                label_sum_tpr[label] += interp(linspace(0, 1, 100), fprs, tprs)

        merged_stat = {}
        for label, sum_tpr in label_sum_tpr.items():
            mean_tpr = sum_tpr / len(stats)
            mean_tpr[0], mean_tpr[1] = 0.0, 1
            interp_auc = auc(linspace(0, 1, 100), mean_tpr)
            logger.debug("interp_auc={0}, individual_auc={1}"
                          .format(interp_auc, individual_auc[label]))

            merged_stat[label] = {
                'auc': interp_auc,
                'fprs': list(linspace(0, 1, 100)),
                'tprs': list(mean_tpr)
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
            formatted.write("ROC-AUC: {0}".format(round(stats['auc'], 3)))
        else:
            # multiple classes
            formatted.write("ROC-AUC:\n")

            table_data = [(repr(label), round(stats[label]['auc'], 3))
                          for label in sorted(stats.keys())]
            formatted.write("".join(["\t" + line + "\n" for line in
                                     tabulate(table_data).split("\n")]))

        return formatted.getvalue()

TestStatistic.register("roc", roc)
