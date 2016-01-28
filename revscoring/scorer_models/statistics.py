"""
A collection of statistics generators that can be applied to
:class:`revscoring.ScorerModel`.

.. autoclass:: roc
    :members:

.. autoclass:: pr
    :members:

.. autoclass:: recall_at_fpr
    :members:

.. autoclass:: filter_rate_at_recall
    :members:

Abstract classes
++++++++++++++++
.. autoclass:: revscoring.scorer_models.statistics.TestStatistic
    :members:

.. autoclass:: revscoring.scorer_models.statistics.ClassStatistic
    :members:
"""
import io
import json
import re

from sklearn.metrics import (auc, average_precision_score,
                             precision_recall_curve, recall_score, roc_curve)
from tabulate import tabulate

from .util import round_or_none

# TODO: This regex fails when commas are used for anything but delimiting
KWARG_STR_RE = re.compile(r"\s*([a-z_][a-z_0-9]*)" +  # 1/1 keyword
                          r"\s*=\s*" +
                          r"([^,\)]+)\s*" +  # 2/2 value
                          r"(,\s*)?")  # 3/3 comma separated

STAT_STR_RE = re.compile(r"\s*([a-z_][a-z_0-9]*)" +  # 1/1 statistic
                         r"(\s*\(" +  # 2 parameters
                            "(" + KWARG_STR_RE.pattern + r")+" +  # 3
                         r"\))?\s*")  # 2 parameters


class TestStatistic:
    """
    Represents a test statistic.
    """
    STATISTICS = {}

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def score(self, scores, labels):
        raise NotImplementedError()

    def format(self, stats):
        raise NotImplementedError()

    def __repr__(self):
        if len(self.kwargs) > 0:
            args = "({0})".format(", ".join(k + "=" + repr(v) for k, v in
                                  self.kwargs.items()))
        else:
            args = ""

        return "{0}{1}".format(self.__class__.__name__, args)

    def __str__(self):
        return self.__repr__()

    def hash(self):
        return hash(self.__str__())

    @classmethod
    def from_stat_str(cls, param_str):
        stat_match = STAT_STR_RE.match(param_str)
        if not stat_match:
            raise ValueError("Malformated statistic string ")
        else:

            kwarg_str = stat_match.group(2) or ""
            class_name = stat_match.group(1)

            if class_name not in cls.STATISTICS:
                raise ValueError("Statistic '{0}' not available"
                                 .format(class_name))
            kwargs = {}
            for kwarg_match in KWARG_STR_RE.finditer(kwarg_str):
                name = kwarg_match.group(1)
                value = json.loads(kwarg_match.group(2))
                kwargs[name] = value

            return cls.STATISTICS[class_name](**kwargs)

    @classmethod
    def register(cls, name, Statistic):
        cls.STATISTICS[name] = Statistic


class ClassStatistic(TestStatistic):
    """
    Represents a test statistic for classifier models.
    """
    def score(self, scores, labels):
        if len(set(labels)) <= 2:
            # Binary classification, class choice doesn't matter.
            comparison_label = max(labels)
            return self._single_class_stat(scores, labels, comparison_label)
        else:
            score = {}
            for comparison_label in set(labels):
                score[comparison_label] = \
                    self._single_class_stat(scores, labels, comparison_label)

            return score


class recall_at_fpr(ClassStatistic):
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
             fpr_score(y_true, [p >= proba for p in y_proba]))
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

    def format(self, stats):
        formatted = io.StringIO()

        if 'threshold' in stats and 'fpr' in stats:
            # Single class
            formatted.write("Recall @ {0} false-positive rate: "
                            .format(self.max_fpr))
            formatted.write("threshold={0}, recall={1}, fpr={2}"
                            .format(round_or_none(stats['threshold'], 3),
                                    round_or_none(stats['recall'], 3),
                                    round_or_none(stats['fpr'], 3)))
        else:
            # multiple classes
            formatted.write("Recall @ {0} false-positive rate:\n"
                            .format(self.max_fpr))

            table_data = [(repr(label),
                           round_or_none(stats[label]['threshold'], 3),
                           round_or_none(stats[label]['recall'], 3),
                           round_or_none(stats[label]['fpr'], 3))
                          for label in sorted(stats.keys())]
            table = tabulate(table_data, headers=["label", "threshold",
                                                  "recall", "fpr"])
            formatted.write("".join(["\t" + line + "\n" for line in
                                     table.split("\n")]))

        return formatted.getvalue()

TestStatistic.register("recall_at_fpr", recall_at_fpr)


def fpr_score(y_true, y_pred):
    true_preds = sum(y_pred) or 1
    return sum(yp and not yt for yt, yp in zip(y_true, y_pred)) / true_preds


class filter_rate_at_recall(ClassStatistic):
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
            (proba, filter_rate_score([p >= proba for p in y_proba]),
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

    def format(self, stats):
        formatted = io.StringIO()

        if 'threshold' in stats and 'filter_rate' in stats:
            # Single class
            formatted.write("Filter rate @ {0} recall: "
                            .format(self.min_recall))
            formatted.write("threshold={0}, filter_rate={1}, recall={2}"
                            .format(round_or_none(stats['threshold'], 3),
                                    round_or_none(stats['filter_rate'], 3),
                                    round_or_none(stats['recall'], 3)))
        else:
            # multiple classes
            formatted.write("Filter rate @ {0} recall:\n"
                            .format(self.min_recall))

            table_data = [(repr(label),
                           round_or_none(stats[label]['threshold'], 3),
                           round_or_none(stats[label]['filter_rate'], 3),
                           round_or_none(stats[label]['recall'], 3))
                          for label in sorted(stats.keys())]
            table = tabulate(table_data, headers=["label", "threshold",
                                                  "filter_rate", "recall"])
            formatted.write("".join(["\t" + line + "\n" for line in
                                     table.split("\n")]))

        return formatted.getvalue()

TestStatistic.register("filter_rate_at_recall", filter_rate_at_recall)


def filter_rate_score(y_pred):
    return 1 - (sum(y_pred) / len(y_pred))


class roc(ClassStatistic):
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
            'tprs': tprs,
            'thresholds': thresholds
        }

    @classmethod
    def format(cls, stats):
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


class pr(ClassStatistic):
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
    def format(cls, stats):
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

TestStatistic.register("pr", pr)
