import logging
from collections import OrderedDict

from tabulate import tabulate

from ... import util
from .scaled_classification_matrix import ScaledClassificationMatrix

logger = logging.getLogger(__name__)


class ScaledPredictionStatistics(ScaledClassificationMatrix):
    FIELDS = ['match_rate', 'filter_rate',
              'precision', '!precision',
              'recall', '!recall',
              'accuracy', 'fpr',
              'f1', '!f1']

    def format_json(self, path_tree, ndigits=3, **kwargs):
        return OrderedDict(
            (field, util.round(self[field], ndigits))
            for field in (path_tree.keys() or self.keys()))

    def format_str(self, path_tree, ndigits=3, **kwargs):
        table_data = [[util.round(self[field], ndigits)
                       for field in path_tree.keys() or self.keys()]]
        return tabulate(table_data, headers=path_tree.keys() or self.keys())

    def __getitem__(self, field):
        if field in self.FIELDS:
            method_name = field.replace("!", "_")
            return getattr(self, method_name)()
        else:
            raise KeyError(field)

    def keys(self):
        return self.FIELDS

    def __iter__(self):
        return iter(self.keys())

    def match_rate(self):
        """
        The proportion of observations that are matched in prediction.

            match-rate = positives / n
        """
        return (self.positives / self.n) if self.n != 0 else None

    def filter_rate(self):
        """
        The proportion of observations that are not matched.

            filter-rate = 1 - match-rate
        """
        return (1 - self.match_rate()) \
            if self.match_rate() is not None else None

    def accuracy(self):
        """
        The proportion of predictions that were right.

            accuracy = correct / n
        """
        return (self.correct / self.n) if self.n != 0 else None

    def recall(self):
        """
        The proportion of the target class that the classifier matches.
        AKA "true-positive rate" and "sensitivity".

            recall = true-positives / target-class
        """
        return (self.tp / self.trues) if self.trues != 0 else None

    def _recall(self):
        """
        The inverse recall.  The proportion of non-target class items that are
        not matched.

            !recall = true-negatives / !target-class
        """
        return (self.tn / self.falses) if self.falses != 0 else None

    def fpr(self):
        """
        False-positive rate.  The proportion of proportion of non-target class
        items that are not matched.

            fpr = false-positives / !target-class
        """
        return (self.fp / self.falses) if self.falses != 0 else None

    def precision(self):
        """
        The proportion of matched observations that are correctly matched.
        AKA "positive predictive value".

            precision = true-positives / true-predicions
        """
        return (self.tp / self.positives) if self.positives != 0 else None

    def _precision(self):
        """
        The proportion of non-matched observations that are correctly not
        matched.  AKA "negative predictive value"

            !precision = true-negatives / false-predictions
        """
        return (self.tn / self.negatives) if self.negatives != 0 else None

    def f1(self):
        """
        An information theoretic statistic that balances specificity with
        sensitivity.
        """
        return (2 * ((self.precision() * self.recall()) /
                     (self.precision() + self.recall()))
                if self.precision() is not None and
                self.recall() is not None and
                self.precision() + self.recall() > 0 else None)

    def _f1(self):
        """
        The inverse f1.  The same information theoretic statistic applied to
        non-matched observations.
        """
        return (2 * ((self._precision() * self._recall()) /
                     (self._precision() + self._recall()))
                if self._precision() is not None and
                self._recall() is not None and
                self._precision() + self._recall() > 0 else None)
